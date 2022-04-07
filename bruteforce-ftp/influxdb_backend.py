# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

__author__ = "Filippo Gaudenzi"
__email__ = "filippo.gaudenzi@moon-cloud.eu"

import requests
import stdout_writer
from config import INFLUXDB_BACKEND_SETTINGS

try:
    from influxdb import InfluxDBClient
except ImportError:
    InfluxDBClient = None


class EvidenceWriter:
    _connection = None
    host = "localhost"
    port = 8086
    database_name = None
    username = None
    password = None
    use_udp = False
    udp_port = None
    use_ssl = False
    verify_ssl = False
    timeout = 120
    SHORT_RETENTION = 'short'
    LONG_RETENTION = 'long'

    def __init__(self, test_id):
        self.options = {}
        self.test_id = test_id
        if not InfluxDBClient:
            raise Exception("Please install the influxdb library to use this celery backend")

        config = INFLUXDB_BACKEND_SETTINGS
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("Please specify influxdb settings in a dictionary")
            config = dict(config)

            self.host = config.pop("host", self.host)
            self.port = config.pop("port", self.port)
            self.database_name = config.pop("database_name", self.database_name)
            self.username = config.pop("username", self.username)
            self.password = config.pop("password", self.password)
            self.use_udp = config.pop("use_udp", self.use_udp)
            self.udp_port = config.pop("udp_port", self.udp_port)
            self.use_ssl = config.pop("use_ssl", self.use_ssl)
            self.verify_ssl = config.pop("verify_ssl", self.verify_ssl)
            self.timeout = config.pop("timeout", self.timeout)

            self.SHORT_RETENTION = config.pop('short_retention', EvidenceWriter.SHORT_RETENTION)
            self.LONG_RETENTION = config.pop('long_retention', EvidenceWriter.LONG_RETENTION)
            try:
                self.url = "influx://{username}:{password}@{hostname}:{port}/{database}".format(
                    username=self.username,
                    password=self.password,
                    hostname=self.host,
                    port=self.port,
                    database=self.database_name
                )
            except Exception:
                print("Please check you influx configuration")

    def _get_connection(self):
        if self._connection is None:
            self._connection = InfluxDBClient(
                host=self.host,
                port=self.port,
                database=self.database_name,
                username=self.username,
                password=self.password,
                use_udp=self.use_udp,
                udp_port=self.udp_port,
                ssl=self.use_ssl,
                verify_ssl=self.verify_ssl,
                timeout=self.timeout
            )
        return self._connection

    def __set(self, value, retention_policy):
        data = {
            "measurement": "evidence",
            "tags": {
                "test_id": self.test_id,
            },

            "fields": value
        }
        self._get_connection().write_points([data], retention_policy=retention_policy)

    def store_result(self, status, extra_data, retention_policy=SHORT_RETENTION):
        data = {'result': bool(status), 'extra-data': json.dumps(extra_data)}
        try:
            self.__set(data, retention_policy=retention_policy)
        except requests.exceptions.ConnectionError:
            stdout_writer.EvidenceWriter().store_result(status, extra_data)
        except Exception as e:
            raise e
        finally:
            pass

