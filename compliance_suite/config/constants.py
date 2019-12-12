# -*- coding: utf-8 -*-
"""Module compliance_suite.config.constants.py

This module contains definitions of project-wide constants for schema file
pointers, API routes, headers, and http request methods
"""

import requests

##################################################
# HTTP METHODS
##################################################

HTTP_GET = 0
HTTP_POST = 1

REQUEST_METHOD = [
    requests.get,
    requests.post
]

##################################################
# MEDIA TYPES
##################################################

DEFAULT_MEDIA_TYPES = [
    'application/vnd.ga4gh.rnaget.v1.0.0+json',
    'application/json'
]

##################################################
# JSON SCHEMAS
##################################################

SCHEMA_RELATIVE_DIR = "schemas"
SCHEMA_FILE_EMPTY = "rnaget-empty.json"
SCHEMA_FILE_EMPTY_ARRAY = "rnaget-empty-array.json"
SCHEMA_FILE_ERROR = "rnaget-error.json"
SCHEMA_FILE_PROJECT = "rnaget-project.json"
SCHEMA_FILE_STUDY = "rnaget-study.json"
SCHEMA_FILE_EXPRESSION = "rnaget-expression.json"
SCHEMA_FILE_CONTINUOUS = "rnaget-continuous.json"
SCHEMA_FILE_SEARCH_FILTER = "rnaget-search-filter.json"
SCHEMA_FILE_SEARCH_FILTER_ARRAY = "rnaget-search-filter-array.json"
SCHEMA_FILE_STRING_ARRAY = "rnaget-string-array.json"
SCHEMA_FILE_TICKET = "rnaget-ticket.json"

##################################################
# API RESOURCES
##################################################

PROJECT_API = 'projects/'
STUDY_API = 'studies/'
EXPRESSION_API = "expressions/"
CONTINUOUS_API = "continuous/"
ENDPOINTS = ["projects", "studies", "expressions", "continuous"]

TEST_RESOURCES = {
    "projects": {
        "9c0eba51095d3939437e220db196e27b": {
            "id": "9c0eba51095d3939437e220db196e27b",
            "filters": {
                "version": "1.0",
                "tags": "RNAgetCompliance",
                "name": "RNAgetTestProject0"
            }
        }
    },
    "studies": {
        "f3ba0b59bed0fa2f1030e7cb508324d1": {
            "id": "f3ba0b59bed0fa2f1030e7cb508324d1",
            "filters": {
                "version": "1.0",
                "tags": "RNAgetCompliance",
                "name": "RNAgetTestStudy0"
            }
        }
    },
    "expressions": {
        "ac3e9279efd02f1c98de4ed3d335b98e": {
            "id": "ac3e9279efd02f1c98de4ed3d335b98e",
            "filters": {
                "version": "1.0",
                "tags": "RNAgetCompliance",
                "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
                "format": "FROM_SERVER"
            }
        }
    },
    "continuous": {
        "5e22e009f41fc53cbea094a41de8798f": {
            "id": "5e22e009f41fc53cbea094a41de8798f",
            "filters": {
                "version": "1.0",
                "tags": "RNAgetCompliance",
                "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
                "format": "FROM_SERVER"
            }
        }
    }
}

##################################################
# STATUS
##################################################

TEST_STATUS_DICT = {
    1: "PASSED",
    0: "SKIPPED",
    -1: "FAILED",
    2: "UNKNOWN ERROR"
}

##################################################
# OTHER
##################################################

NONEXISTENT_ID = "nonexistentid9999999999999999999"