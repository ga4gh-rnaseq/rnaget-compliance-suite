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
    
    NOT_IMPLEMENTED_TEST_GRAPH (dict): graph of parent-child test relationships
        when the endpoint is not implemented by the server. Not implemented
        endpoints must still be tested to ensure that they yield the correct
        status code
        key: string of parent test name
        value: dictionary of child tests
"""

TEST_GRAPH = {
    "projects": {
        "base": {
            "project_get": {
                "project_get_default": {},
                "project_get_not_found": {}
            },

            "project_search": {
                "project_search_url_params_all": {},
                "project_search_url_params_cases": {},
                "project_search_filters": {}
            }
        }
    },
    "studies": {
        "base": {
            "study_get": {
                "study_get_default": {},
                "study_get_not_found": {}
            },

            "study_search": {
                "study_search_url_params_all": {},
                "study_search_url_params_cases": {},
                "study_search_filters": {}
            }
        }
    },
    "expressions": {
        "base": {
            "expression_get": {
                "expression_get_default": {},
                "expression_get_not_found": {}
            },
            "expression_formats": {},
            "expression_search": {
                "expression_search_url_params_all": {},
                "expression_search_url_params_cases": {},
                "expression_search_filters": {}
            }
        }
    },
    "continuous": {
        "base": {
            "continuous_get": {
                "continuous_get_default": {},
                "continuous_get_not_found": {}
            }
        }
    }
}
"""dict: hierarchical graph of parent-child test relationships"""

NOT_IMPLEMENTED_TEST_GRAPH = {
    "projects": {
        "base": {
            "project_endpoint_not_implemented": {}
        }
    },
    "studies": {
        "base": {
            "study_endpoint_not_implemented": {}
        }
    },
    "expressions": {
        "base": {
            "expression_endpoint_not_implemented": {}
        }
    },
    "continuous": {
        "base": {
            "continuous_endpoint_not_implemented": {}
        }
    }
}
"""dict: parent-child test relationships when endpoint not implemented"""