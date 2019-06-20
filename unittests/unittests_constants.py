# -*- coding: utf-8 -*-
"""Module unittests.unittests_constants.py

This module contains constant data structures to be accessed by multiple
unit testing modules.

Attributes:
    SERVER_CONFIG (dict): complete, correct user config dictionary
    SERVER_CONFIG_NOT_IMPLEMENTED (dict): config without implemented endpoints 
"""

SERVER_CONFIG = {
    "server_name": "Server A",
    "base_url": "http://localhost:5000/",
    "token": "gd3uhUnyk3pVVDakkPSK7Pa0V7EvuOCa",
    "implemented": {
        "projects": True,
        "studies": True,
        "expressions": True,
        "continuous": False
    },
    "projects": [
        {
            "id": "43378a5d48364f9d8cf3c3d5104df560",
            "filters": {
                "version": "1.0",
                "name": "PCAWG"
            }
        }, {
            "id": "123456789",
            "filters": {
                "version": "2.0",
                "name": "Non-existent Dataset"
            }
        }, {
            "id": "38n54mgtogq4nq2s5nfqcoop4160vso7",
            "filters": {
                "version": "2.0",
                "name": "Bad Schema File"
            }
        }
    ],
    "studies": [
        {
            "id": "6cccbbd76b9c4837bd7342dd616d0fec",
            "filters": {
                "version": "1.0",
                "name": "PCAWG"
            }
        }
    ],
    "expressions": [
        {
            "id": "2a7ab5533ef941eaa59edbfe887b58c4",
            "filters": {
                "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
                "format": "loom"
            }
        }
    ],
    "continuous": [
        {
            "id": "9999",
            "filters": {
                "version": "1.0",
                "name": "PCAWG"
            }
        }
    ]
}
"""complete, correct user config dictionary, as if parsed from yaml file"""

SERVER_CONFIG_NOT_IMPLEMENTED = {
    "server_name": "Server A",
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