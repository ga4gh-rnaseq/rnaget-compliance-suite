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
                "project_get_not_found": {}
            },

            "project_search": {
                "project_search_filters": {},
                "project_search_url_params_all": {},
                "project_search_url_params_cases": {},
                "project_search_filters_out": {}
                
            }
        }
    },
    "studies": {
        "base": {
            "study_get": {
                "study_get_not_found": {}
            },

            "study_search": {
                "study_search_filters": {},
                "study_search_url_params_all": {},
                "study_search_url_params_cases": {},
                "study_search_filters_out": {}
            }
        }
    },
    "expressions": {
        "base": {
            "expression_get": {
                "expression_get_not_found": {},
                "expression_get_content": {},
                "expression_formats": {},
                "expression_search": {
                    "expression_search_filters": {},
                    "expression_search_url_params_all": {},
                    "expression_search_url_params_cases": {},
                    "expression_search_filters_out": {},
                    "expression_search_format_not_specified": {},
                    "expression_search_filetypes_match": {},
                    "expression_search_no_filetype_mismatches": {}
                }
            }
        }
    },
    "continuous": {
        "base": {
            "continuous_get": {
                "continuous_get_not_found": {},
                "continuous_formats": {},
                "continuous_search": {
                    "continuous_search_filters": {},
                    "continuous_search_url_params_all": {},
                    "continuous_search_url_params_cases": {},
                    "continuous_search_filters_out": {},
                    "continuous_search_format_not_specified": {},
                    "continuous_search_formats_match": {},
                    "continuous_search_no_format_mismatches": {}
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