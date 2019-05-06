# -*- coding: utf-8 -*-
"""Module compliance_suite.config.graph.py

This module contains a single dictionary, which represents the parent-child
hierarchical relationship of all test cases. Child tests will be skipped if
parent tests fail. Each test name in the graph corresponds to a test outlined
in compliance_suite.config.tests.py. The "name" attribute in the tests.py config
is equivalent to keys in the below graph.

Attributes:
    TEST_GRAPH (dict): hierarchical graph of parent-child test relationships
        key: string of parent test name
        value: dictionary of child tests

"""

TEST_GRAPH = {
    "base": {
        "project_get": {
            "project_get_default": {}
        },

        "project_search": {
            "project_search_url_params": {},
            "project_search_filters": {},
            "project_search_url_params_cases": {}
        },

        "study_get": {
            "study_get_default": {}
        },

        "study_search": {
            "study_search_url_params": {},
            "study_search_url_params_cases": {},
            "study_search_filters": {}
        },

        "expression_get": {
            "expression_get_default": {}
        }
    }
}
"""dict: hierarchical graph of parent-child test relationships"""