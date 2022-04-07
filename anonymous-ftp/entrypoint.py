#!/usr/bin/env python
import json
import logging
import sys

from driver import Driver

try:
    with open('test/metadata.json', 'r') as data_file:
        data = json.load(data_file)
except IOError:
    logging.error("Unable to find 'metadata.json'")
    sys.exit(-1)

driver_name = data.get("driver-name", None)
if not driver_name:
    logging.error("Driver name not specified in 'metadata.json'")
    sys.exit(-1)

run_delay = data.get("run-delay", None)
aggregation_step = data.get("aggregation-step", None)
try:
    Driver.load("test/")
except ImportError:
    logging.error("I was unable to find the driver '%s'" % driver_name)
    sys.exit(-1)

if not len(Driver.registered):
    logging.error("I was unable to load the driver '%s'" % driver_name)
    sys.exit(-1)

try:
    testcase = json.load(sys.stdin)
except ValueError:
    logging.error("Invalid JSON provided in STDIN")
    sys.exit(-1)

this_driver = [x for x in Driver.registered if x.__name__ == driver_name][0]
this_driver_instance = this_driver(testcase, run_delay, aggregation_step)
this_driver_instance.appendAtomics()
print(this_driver_instance.run)
