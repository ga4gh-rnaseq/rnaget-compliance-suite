# -*- coding: utf-8 -*-
"""Module unittests.constants.py

This module contains constant data structures to be accessed by multiple
unit testing modules.

Attributes:
    OUTPUT_DIR (str): sample output directory to write to for unit tests
    SERVER_CONFIG (dict): complete, correct user config dictionary
    SERVER_CONFIG_NOT_IMPLEMENTED (dict): config without implemented endpoints 
"""

DEFAULT_OUTPUT_DIR = "./rnaget-compliance-results"
DEFAULT_OUTPUT_ARCHIVE = DEFAULT_OUTPUT_DIR + ".tar.gz"
OUTPUT_DIR = "unittests/data/results/temp_result"
OUTPUT_ARCHIVE = OUTPUT_DIR + ".tar.gz"

SERVER_CONFIG = {
    "server_name": "Unit Test Server",
    "base_url": "http://localhost:5000/",
    "token": "gd3uhUnyk3pVVDakkPSK7Pa0V7EvuOCa",
    "implemented": {
        "projects": True,
        "studies": True,
        "expressions": True,
        "continuous": True
    }
}
"""complete, correct user config dictionary, as if parsed from yaml file"""

SERVER_CONFIG_NOT_IMPLEMENTED = {
    "server_name": "Not Implemented Server",
    "base_url": "http://localhost:5000/",
    "token": "gd3uhUnyk3pVVDakkPSK7Pa0V7EvuOCa",
    "implemented": {
        "projects": False,
        "studies": False,
        "expressions": False,
        "continuous": False
    }
}
"""user config dictionary as if parsed from yaml file, without any endpoints"""