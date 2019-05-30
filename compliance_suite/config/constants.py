# -*- coding: utf-8 -*-
"""Module compliance_suite.config.constants.py

This module contains definitions of project-wide constants for schema file
pointers, API routes, headers, and http request methods

Attributes:
    HTTP_GET (int): integer corresponding to get request method
    HTTP_POST (int): integer corresponding to post request method
    REQUEST_METHOD (list): references to request library methods get and post
    ACCEPT_HEADER (dict): dict of accepted request headers
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

ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.rnaget.v1.0.0+json'
}

SCHEMA_RELATIVE_DIR = "schemas"
SCHEMA_FILE_EMPTY = "rnaget-empty.json"
SCHEMA_FILE_PROJECT = "rnaget-project.json"
SCHEMA_FILE_STUDY = "rnaget-study.json"
SCHEMA_FILE_EXPRESSION = "rnaget-expression.json"
SCHEMA_FILE_SEARCH_FILTER = "rnaget-search-filter.json"
SCHEMA_FILE_PROJECT_ARRAY = "rnaget-project-array.json"
SCHEMA_FILE_STUDY_ARRAY = "rnaget-study-array.json"
SCHEMA_FILE_EXPRESSION_ARRAY = "rnaget-expression-array.json"
SCHEMA_FILE_SEARCH_FILTER_ARRAY = "rnaget-search-filter-array.json"

PROJECT_API = 'projects/'
STUDY_API = 'studies/'
EXPRESSION_API = "expressions/"

ENDPOINTS = ["projects", "studies", "expressions"]

NONEXISTENT_ID = "999999999"
