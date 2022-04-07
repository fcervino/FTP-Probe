# -*- coding: utf-8 -*-
import copy
import importlib
import importlib.util
import json
import logging
import os
import pkgutil
import time
import traceback

from StopChecker import RedisStopChecker
from config import TEST_ID
from influxdb_backend import EvidenceWriter


class AtomicOperation(object):
    action = None
    rollback = None

    def __init__(self, action, rollback):
        self.action = action
        self.rollback = rollback


class ExitStatus(object):
    status = 0
    __message = ["Successfully Ended", "Soft Kill", "Hard Kill"]

    def __repr__(self):
        serialized = {
            "status": self.status,
            "message": self.__message[self.status],
        }

        return json.dumps(serialized)

    def set_status_exit(self, status):
        self.status = status


class DriverResult(object):
    result = None
    __data = {}

    def __repr__(self):
        serialized = {
            "result": self.result,
            "data": self.__data,
        }

        return json.dumps(serialized)

    def put_value(self, key, value=""):
        self.__data[key] = value

    def clear_values(self):
        self.__data = {}
        self.result = []

    def get_value(self, key, default=None):
        return self.__data.get(key, default)

    def get_extradata(self):
        return self.__data


class MetaDriver(type):
    def __init__(cls, name, base, attrs):
        if not hasattr(cls, 'registered'):
            cls.registered = []
        else:
            cls.registered.append(cls)


class Driver(object, metaclass=MetaDriver):

    @classmethod
    def load(cls, *paths):
        cls.registered = []
        for _, name, _ in pkgutil.iter_modules(paths):
            package = os.path.dirname(paths[0])
            try:
                importlib.import_module("." + name, package)
            except Exception as e:
                print(e)

    def __init__(self, testinstances, frequency=None, aggregation_step=None):
        self.testinstances = testinstances
        self.result = DriverResult()
        self.frequency = frequency
        self.aggregation_step = aggregation_step
        self.exit = ExitStatus()
        self.atomic_operations = []
        self.aggregation_operation = []
        self.error = False
        self.all_evidence = []

        self.stop_checker = RedisStopChecker()
        self.environ_stop = os.getenv("STOP", 0)

    def appendAtomic(self, action, rollback):
        self.atomic_operations.append(AtomicOperation(action, rollback))

    def aggregation_op(self, action):
        self.aggregation_operation.append(AtomicOperation(action, lambda: None))

    @property
    def run(self):
        writer = EvidenceWriter(TEST_ID)
        prev_out = None
        ctr = 0
        n_op = 0
        while True:
            self.result.clear_values()
            try:
                for operation in self.atomic_operations:
                    out = operation.action(prev_out)
                    prev_out = out
                    ctr += 1
                logging.info("Test execution finished")
                self.result.result = prev_out
            except Exception as e:
                error_message = "Phase {} returned an exception. Reverting operations. Stepping back to {}".format(
                    str(ctr), str(ctr - 1))
                logging.critical(len(self.atomic_operations))
                logging.error(error_message)
                logging.error("Exception: " + traceback.format_exc())
                self.result.put_value('error', {'message': error_message, 'exception': str(e)})

                try:
                    rollback_prev_out = prev_out
                    for rollback in range(ctr % len(self.atomic_operations), -1, -1):
                        rollback_prev_out = self.atomic_operations[ctr % len(self.atomic_operations)].rollback(
                            rollback_prev_out)
                        ctr -= 1

                except Exception as e2:
                    nested_error_message = "Exception during rollback at phase {}".format(str(ctr))
                    logging.critical(nested_error_message)
                    logging.critical(traceback.format_exc())
                    self.result.result = False
                    self.result.put_value('error2', {'message': error_message, 'exception': str(e2)})
                finally:
                    self.exit.set_status_exit(2)
                    break
            finally:
                self.all_evidence.append(copy.copy(self.result))

                n_op += 1
                print(self.aggregation_operation)
                if len(self.aggregation_operation) > 0 and n_op == self.aggregation_step:
                    # Aggregation Step, Long retention
                    if len(self.aggregation_operation) == 0:
                        logging.critical("Exception during aggregation, no aggregation found")
                    for operation in self.aggregation_operation:
                        self.result.clear_values()
                        out = operation.action(self.all_evidence)
                        writer.store_result(out, self.result.get_extradata(), retention_policy=writer.LONG_RETENTION)
                    self.all_evidence.clear()
                    n_op = 0
                elif len(self.aggregation_operation) > 0:
                    # Write in short_retention by default
                    writer.store_result(self.result.result, self.result.get_extradata())
                elif len(self.aggregation_operation) == 0:
                    writer.store_result(self.result.result, self.result.get_extradata(),
                                        retention_policy=writer.LONG_RETENTION)
                if self.environ_stop == '1' or self.stop_checker.check_stop():
                    print("TEST SHOULD TERMINATE")
                    self.exit.set_status_exit(1)
                    break
            if self.frequency:
                time.sleep(self.frequency)
            else:
                break
        return self.exit
