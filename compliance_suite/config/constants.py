# -*- coding: utf-8 -*-
"""Module compliance_suite.config.constants.py

This module contains definitions of project-wide constants for schema file
pointers, API routes, headers, and http request methods

Attributes:
    HTTP_GET (int): integer corresponding to get request method
    HTTP_POST (int): integer corresponding to post request method
    REQUEST_METHOD (list): references to request library methods get and post
    DEFAULT_MEDIA_TYPES (list): media types in request header "Accept"
    SCHEMA_RELATIVE_DIR (str): path to schema directory
    SCHEMA_FILE_PROJECT (str): filename for project schema
    SCHEMA_FILE_STUDY (str): filename for study schema
    SCHEMA_FILE_EXPRESSION (str): filename for expression schema
    SCHEMA_FILE_SEARCH_FILTER (str): filename for search filter schema
    SCHEMA_FILE_PROJECT_ARRAY (str): filename for project array schema
    SCHEMA_FILE_STUDY_ARRAY (str): filename for study array schema
    SCHEMA_FILE_EXPRESSION_ARRAY (str): filename for expression array schema
    SCHEMA_FILE_SEARCH_FILTER_ARRAY (str): filename for filter array schema
    PROJECT_API (str): api route for project-related requests
    STUDY_API (str): api route for study-related requests
    EXPRESSION_API (str): api route for expression-related requests
    ENDPOINTS (list): all endpoints/object types
    NONEXISTENT_ID (str): id for requesting api objects that do not exist
        on the host server
"""

import requests

HTTP_GET = 0
HTTP_POST = 1

REQUEST_METHOD = [
    requests.get,
    requests.post
]

DEFAULT_MEDIA_TYPES = [
    'application/vnd.ga4gh.rnaget.v1.0.0+json',
    'application/json'
]

SCHEMA_RELATIVE_DIR = "schemas"
SCHEMA_FILE_EMPTY = "rnaget-empty.json"
SCHEMA_FILE_EMPTY_ARRAY = "rnaget-empty-array.json"
SCHEMA_FILE_ERROR = "rnaget-error.json"
SCHEMA_FILE_PROJECT = "rnaget-project.json"
SCHEMA_FILE_STUDY = "rnaget-study.json"
SCHEMA_FILE_EXPRESSION = "rnaget-expression.json"
SCHEMA_FILE_EXPRESSION_LOOM = "rnaget-expression-loom.json"
SCHEMA_FILE_EXPRESSION_TSV = "rnaget-expression-tsv.json"
SCHEMA_FILE_CONTINUOUS = "rnaget-continuous.json"
SCHEMA_FILE_SEARCH_FILTER = "rnaget-search-filter.json"
SCHEMA_FILE_PROJECT_ARRAY = "rnaget-project-array.json"
SCHEMA_FILE_PROJECT_ARRAY_FULL = "rnaget-project-array-full.json"
SCHEMA_FILE_STUDY_ARRAY = "rnaget-study-array.json"
SCHEMA_FILE_STUDY_ARRAY_FULL = "rnaget-study-array-full.json"
SCHEMA_FILE_EXPRESSION_ARRAY = "rnaget-expression-array.json"
SCHEMA_FILE_EXPRESSION_ARRAY_FULL = "rnaget-expression-array-full.json"
SCHEMA_FILE_EXPRESSION_LOOM_ARRAY = "rnaget-expression-loom-array.json"
SCHEMA_FILE_EXPRESSION_LOOM_ARRAY_FULL = "rnaget-expression-loom-array-full" \
                                         + ".json"
SCHEMA_FILE_EXPRESSION_TSV_ARRAY = "rnaget-expression-tsv-array.json"
SCHEMA_FILE_EXPRESSION_TSV_ARRAY_FULL = "rnaget-expression-tsv-array-full.json"

SCHEMA_FILE_EXPRESSION_FORMAT_TEMPLATE = \
    "rnaget-expression-format-template.json"
SCHEMA_FILE_EXPRESSION_ARRAY_FORMAT_TEMPLATE = \
    "rnaget-expression-array-format-template.json"

SCHEMA_FILE_CONTINUOUS_ARRAY = "rnaget-continuous-array.json"
SCHEMA_FILE_CONTINUOUS_ARRAY_FULL = "rnaget-continuous-array-full.json"
SCHEMA_FILE_CONTINUOUS_FORMAT_TEMPLATE = \
    "rnaget-continuous-format-template.json"
SCHEMA_FILE_CONTINUOUS_ARRAY_FORMAT_TEMPLATE = \
    "rnaget-continuous-array-format-template.json"

SCHEMA_FILE_SEARCH_FILTER_ARRAY = "rnaget-search-filter-array.json"
SCHEMA_FILE_STRING_ARRAY = "rnaget-string-array.json"

PROJECT_API = 'projects/'
STUDY_API = 'studies/'
EXPRESSION_API = "expressions/"
CONTINUOUS_API = "continuous/"

ENDPOINTS = ["projects", "studies", "expressions", "continuous"]
TEST_RESOURCES = {
    "projects": [
        {
            "id": "9c0eba51095d3939437e220db196e27b",
            "filters": {
                "version": "1.0",
                "tags": "RNAgetCompliance",
                "name": "RNAgetTestProject0"
            }
        }
    ],
    "studies": [
        {
            "id": "f3ba0b59bed0fa2f1030e7cb508324d1",
            "filters": {
                "version": "1.0",
                "tags": "RNAgetCompliance",
                "name": "RNAgetTestStudy0"
            }
        }
    ],
    "expressions": [
        {
            "id": "ac3e9279efd02f1c98de4ed3d335b98e",
            "filters": {
                "version": "1.0",
                "tags": "RNAgetCompliance",
                "format": "FROM_SERVER"
            }
        }
    ],
    "continuous": [
        {
            "id": "5e22e009f41fc53cbea094a41de8798f",
            "filters": {
                "version": "1.0",
                "tags": "RNAgetCompliance",
                "format": "FROM_SERVER"
            }
        }
    ]
}

NONEXISTENT_ID = "nonexistentid9999999999999999999"