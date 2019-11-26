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
            "project_get": {},
            "project_filters": {
                "project_search": {}
            }
        }
    },
    "studies": {
        "base": {
            "study_get": {},
            "study_filters": {
                "study_search": {}
            }
        }
    },
    "expressions": {
        "base": {
            "expression_formats": {
                "single_expression_ticket": {},
                "single_expression_bytes": {},
                "expression_filters": {
                    "multi_expression_ticket": {},
                    "multi_expression_bytes": {}
                }
            }
        }
    },
    "continuous": {
        "base": {
            "continuous_formats": {
                "single_continuous_ticket": {},
                "single_continuous_bytes": {},
                "continuous_filters": {
                    "multi_continuous_ticket": {},
                    "multi_continuous_bytes": {}
                }
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
