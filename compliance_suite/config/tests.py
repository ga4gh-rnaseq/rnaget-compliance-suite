# -*- coding: utf-8 -*-
"""Module compliance_suite.config.tests.py

This module contains all test scenarios as a hierarchical dictionary.

In TESTS_DICT, each value is passed to a TestExecutor, each key is the test name
Each value under TESTS_DICT[key]["api"] is passed to APIComponent
Each value under TESTS_DICT[key]["content"] is passed to ContentComponent
Each value under TESTS_DICT[key]["api"]["cases"] is passed to APICase
Each value under TESTS_DICT[key]["content"]["cases"] is passed to ContentCase

Each class is able to handle the parameters passed to it.

Attributes:
    TESTS_DICT (dict): attributes for all test scenarios as a hierarchical dict.
    TESTS_BY_OBJECT_TYPE (dict): lists the name of tests grouped by the object
        type they pertain to (project, study, expression)
    NOT_IMPLEMENTED_TESTS_BY_OBJECT_TYPE (dict): lists the name of tests
        associated with non-implemented endpoints, grouped by the object type
        they pertain to. Non-implemented endpoints must still be correctly
        configured, ie must yield 501 response.
"""

import compliance_suite.config.constants as c
import compliance_suite.functions.schema as sf
import compliance_suite.functions.parameter as pf
import compliance_suite.functions.content_testing as cf
import compliance_suite.functions.update_server_settings as uf

TESTS_DICT = {
    "project_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT GET
        # # # # # # # # # # # # # # # # # # # # 
        "name": "project_get",
        "description": "Requests the /projects/:id endpoint",
        "pass_text": "'Get Project by Id' endpoint correctly implemented",
        "fail_text": "'Get Project by Id' endpoint NOT correctly implemented",
        "skip_text": "'Get Project by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Project",
                    "description": "request /projects/:id using test project "
                        + "id. checks content type and status code "
                        + "(200). validates response body matches "
                        + "Project object schema.",
                    "summary_pass": "Test project successfully retrieved",
                    "summary_fail": "Test project NOT retrieved",
                    "summary_skip": "'Get Test Project' skipped",
                    "url": c.PROJECT_API + "V_PROJECT_ID",
                    "schema_func": sf.schema_require_matching_id
                },

                {
                    "name": "Project Not Found",
                    "description": "request /projects/:id using a project id "
                        + "known to not exist. Checks content type and status "
                        + "code (4xx). Validates response body matches Error "
                        + "schema.",
                    "summary_pass": "Server sends correct response when "
                        + "requested project not found",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when requested project not found",
                    "summary_skip": "'Project Not Found' skipped",
                    "url": c.PROJECT_API + c.NONEXISTENT_ID,
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
                }
            ]
        }
    }, "project_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_filters",
        "description": "requests the /projects/search/filters endpoint",
        "pass_text": "'Project Search Filters' endpoint correctly implemented",
        "fail_text": "'Project Search Filters' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Project Search Filters' test skipped",

        "api": {
            "global_properties": {
                "url": c.PROJECT_API + "search/filters",
                "http_method": c.HTTP_GET,
                "request_params": {},
                "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
                "server_settings_update_func": uf.update_supported_filters
            },

            "cases": [
                {
                    "name": "Project Search Filters",
                    "description": "request /projects/search/filters. checks "
                        + "content type and status code (200). "
                        + "validates response body matches search "
                        + "filter array schema.",
                    "summary_pass": "Project search filters successfully "
                        + "retrieved",
                    "summary_fail": "Project search filters NOT retrieved",
                    "summary_skip": "'Project Search Filters' skipped",
                }
            ]
        }
    }, "project_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search",
        "description": "Requests the /projects/search endpoint",
        "pass_text": "'Project Search' endpoint correctly implemented",
        "fail_text": "'Project Search' endpoint NOT correctly implemented",
        "skip_text": "'Project Search' test skipped",

        "api": {
            "global_properties": {
                "url": c.PROJECT_API + "search",
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Search Projects Without Filters",
                    "description": "request /projects/search without any "
                        + "parameter filters. checks content type "
                        + "and status code (200). validates "
                        + "response body matches project array "
                        + "schema.",
                    "summary_pass": "Projects can be searched without filters",
                    "summary_fail": "Projects CANNOT be searched without "
                        + "filters",
                    "summary_skip": "'Search Projects Without Filters' skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params": {}
                },

                {
                    "name": "Search Projects With All Filters",
                    "description": "request /projects/search using all "
                        + "server-supported project filters. checks content "
                        + "type and status code (200). validates response body "
                        + "matches project array schema.",
                    "summary_pass": "Projects can be searched with all filters "
                        + "specified",
                    "summary_fail": "Projects CANNOT be searched with all "
                        + "filters specified",
                    "summary_skip": "'Search Projects With All Filters' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.all_supported_filters
                },

                {
                    "name": "Search Projects With Single Filter, 1",
                    "description": "request /projects/search using the first "
                        + "parameter filter supported by server. checks "
                        + "type and status code (200). validates response body "
                        + "matches project array schema",
                    "summary_pass": "Projects can be searched when first "
                        + "filter parameter is supplied",
                    "summary_fail": "Projects CANNOT be searched when first "
                        + "filter parameter is supplied",
                    "summary_skip": "'Search Projects With Single Filter, 1' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.first_supported_filter
                },

                {
                    "name": "Search Projects With Single Filter, 2",
                    "description": "request /projects/search using the second "
                        + "parameter filter supported by server. checks "
                        + "type and status code (200). validates response body "
                        + "matches project array schema",
                    "summary_pass": "Projects can be searched when second "
                        + "filter parameter is supplied",
                    "summary_fail": "Projects CANNOT be searched when second "
                        + "filter parameter is supplied",
                    "summary_skip": "'Search Projects With Single Filter, 2' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.second_supported_filter
                },

                {
                    "name": "Project Search Filters Non-Matching Resources",
                    "description": "request /projects/search using filters "
                        + "that do not apply to any project. "
                        + "checks content type and status code (200). "
                        + "validates response body is an empty array.",
                    "summary_pass": "Project search endpoint filters "
                        + "non-matching resources",
                    "summary_fail": "Project search endpoint DOES NOT filter "
                        + "non-matching resources",
                    "summary_skip": "'Project Search Filters Non-Matching "
                        + "Resources' skipped",
                    "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
                    "request_params_func": pf.incorrect_filter_values
                }
            ]
        }
    }, "project_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "project_endpoint_not_implemented",
        "description": "Requests various /projects routes, expecting the "
                       + "service to respond with a 'Not Implemented' status "
                       + "code",
        "pass_text": "Project endpoints correctly non-implemented",
        "fail_text": "Project endpoints NOT correctly non-implemented",
        "skip_text": "Project endpoints not implemented test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {},
                "expected_status": [501],
                "schema_file": c.SCHEMA_FILE_EMPTY
            },

            "cases": [
                {
                    "name": "Project Get Not Implemented",
                    "description": "request /projects/:id, expecting "
                                   + "501 status code",
                    "summary_pass": "Project Get correctly non-implemented",
                    "summary_fail": "Project Get NOT correctly non-implemented",
                    "summary_skip": "'Project Get Not Implemented' skipped",
                    "url": c.PROJECT_API + c.NONEXISTENT_ID
                },

                {
                    "name": "Project Search Not Implemented",
                    "description": "request /projects/search, expecting 501 "
                        + "status code",
                    "summary_pass": "Project Search correctly non-implemented",
                    "summary_fail": "Project Search NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Project Search Not Implemented' skipped",
                    "url": c.PROJECT_API + "search"
                },

                {
                    "name": "Project Search Filters Not Implemented",
                    "description": "request /projects/search/filters, "
                        + "expecting 501 status code",
                    "summary_pass": "Project Search Filters correctly "
                        + "non-implemented",
                    "summary_fail": "Project Search Filters NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Project Search Filters Not Implemented' "
                        + "skipped",
                    "url": c.PROJECT_API + "search/filters"
                }
            ]
        }
    }, "study_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY GET
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_get",
        "description": "Requests the /studies/id endpoint",
        "pass_text": "'Get Study by Id' endpoint correctly implemented",
        "fail_text": "'Get Study by Id' endpoint NOT correctly implemented",
        "skip_text": "'Get Study by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Study",
                    "description": "request /studies/:id using test study id. "
                        + "checks content type and status code (200). "
                        + "validates response body matches Study "
                        + "object schema.",
                    "summary_pass": "Test study successfully retrieved",
                    "summary_fail": "Test study NOT retrieved",
                    "summary_skip": "'Get Test Study' skipped",
                    "url": c.STUDY_API + "V_STUDY_ID",
                    "schema_func": sf.schema_require_matching_id
                },

                {
                    "name": "Study Not Found",
                    "description": "request /studies/:id using a study id "
                        + "known to not exist. Checks content type and status "
                        + "code (4xx). Validates response body matches Error "
                        + "schema.",
                    "summary_pass": "Server sends correct response when "
                        + "requested study not found",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when requested study not found",
                    "summary_skip": "'Study Not Found' skipped",
                    "url": c.STUDY_API + c.NONEXISTENT_ID,
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
                }
            ]
        }
    }, "study_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_filters",
        "description": "requests the /studies/search/filters endpoint",
        "pass_text": "'Study Search Filters' endpoint correctly implemented",
        "fail_text": "'Study Search Filters' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Study Search Filters' test skipped",

        "api": {
            "global_properties": {
                "url": c.STUDY_API + "search/filters",
                "http_method": c.HTTP_GET,
                "request_params": {},
                "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
                "server_settings_update_func": uf.update_supported_filters
            },

            "cases": [
                {
                    "name": "Study Search Filters",
                    "description": "request /studies/search/filters. checks "
                        + "content type and status code (200). "
                        + "validates response body matches search "
                        + "filter array schema.",
                    "summary_pass": "Study search filters successfully "
                        + "retrieved",
                    "summary_fail": "Study search filters NOT retrieved",
                    "summary_skip": "'Study Search Filters' skipped",
                }
            ]
        }
    }, "study_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search",
        "description": "Requests the /studies/search endpoint",
        "pass_text": "'Study Search' endpoint correctly implemented",
        "fail_text": "'Study Search' endpoint NOT correctly implemented",
        "skip_text": "'Study Search' test skipped",

        "api": {
            "global_properties": {
                "url": c.STUDY_API + "search",
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Search Studies Without Filters",
                    "description": "request /studies/search without any "
                        + "parameter filters. checks content type "
                        + "and status code (200). validates "
                        + "response body matches study array "
                        + "schema.",
                    "summary_pass": "Studies can be searched without filters",
                    "summary_fail": "Studies CANNOT be searched without "
                        + "filters",
                    "summary_skip": "'Search Studies Without Filters' skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params": {}
                },

                {
                    "name": "Search Studies With All Filters",
                    "description": "request /studies/search using all "
                        + "server-supported study filters. checks content "
                        + "type and status code (200). validates response body "
                        + "matches study array schema.",
                    "summary_pass": "Studies can be searched with all filters "
                        + "specified",
                    "summary_fail": "Studies CANNOT be searched with all "
                        + "filters specified",
                    "summary_skip": "'Search Studies With All Filters' skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.all_supported_filters
                },

                {
                    "name": "Search Studies With Single Filter, 1",
                    "description": "request /studies/search using the first "
                        + "parameter filter supported by server. checks "
                        + "type and status code (200). validates response body "
                        + "matches study array schema",
                    "summary_pass": "Studies can be searched when first filter "
                        + "parameter is supplied",
                    "summary_fail": "Studies CANNOT be searched when first "
                        + "filter parameter is supplied",
                    "summary_skip": "'Search Studies With Single Filter, 1' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.first_supported_filter
                },

                {
                    "name": "Search Studies With Single Filter, 2",
                    "description": "request /studies/search using the second "
                        + "parameter filter supported by server. checks "
                        + "type and status code (200). validates response body "
                        + "matches study array schema",
                    "summary_pass": "Studies can be searched when second "
                        + "filter parameter is supplied",
                    "summary_fail": "Studies CANNOT be searched when second "
                        + "filter parameter is supplied",
                    "summary_skip": "'Search Studies With Single Filter, 2' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.second_supported_filter
                },

                {
                    "name": "Study Search Filters Non-Matching Resources",
                    "description": "request /studies/search using filters "
                        + "that do not apply to any project. "
                        + "checks content type and status code (200). "
                        + "validates response body is an empty array.",
                    "summary_pass": "Study search endpoint filters "
                        + "non-matching resources",
                    "summary_fail": "Study search endpoint DOES NOT filter "
                        + "non-matching resources",
                    "summary_skip": "'Study Search Filters Non-Matching "
                        + "Resources' skipped",
                    "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
                    "request_params_func": pf.incorrect_filter_values
                }
            ]
        }
    }, "study_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "study_endpoint_not_implemented",
        "description": "Requests various /studies routes, expecting the "
                       + "service to respond with a 'Not Implemented' status "
                       + "code",
        "pass_text": "Study endpoints correctly non-implemented",
        "fail_text": "Study endpoints NOT correctly non-implemented",
        "skip_text": "Study endpoints not implemented test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {},
                "expected_status": [501],
                "schema_file": c.SCHEMA_FILE_EMPTY
            },

            "cases": [
                {
                    "name": "Study Get Not Implemented",
                    "description": "request /studies/:id, expecting "
                                   + "501 status code",
                    "summary_pass": "Study Get correctly non-implemented",
                    "summary_fail": "Study Get NOT correctly non-implemented",
                    "summary_skip": "'Study Get Not Implemented' skipped",
                    "url": c.STUDY_API + c.NONEXISTENT_ID
                },

                {
                    "name": "Study Search Not Implemented",
                    "description": "request /studies/search, expecting 501 "
                                   + "status code",
                    "summary_pass": "Study Search correctly non-implemented",
                    "summary_fail": "Study Search NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Study Search Not Implemented' skipped",
                    "url": c.STUDY_API + "search"
                },

                {
                    "name": "Study Search Filters Not Implemented",
                    "description": "request /studies/search/filters, "
                        + "expecting 501 status code",
                    "summary_pass": "Study Search Filters correctly "
                        + "non-implemented",
                    "summary_fail": "Study Search Filters NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Study Search Filters Not Implemented' "
                        + "skipped",
                    "url": c.STUDY_API + "search/filters"
                }
            ]
        }
    }, "expression_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION GET
        # # # # # # # # # # # # # # # # # # # # 
        "name": "expression_get",
        "description": "Requests the /expressions/:id endpoint",
        "pass_text": "'Get Expression by Id' endpoint correctly implemented",
        "fail_text": "'Get Expression by Id' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Get Expression by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Expression",
                    "description": "request /expressions/:id using test "
                        + "expression id. checks content type and status code "
                        + "(200). validates response body matches Expression "
                        + "object schema.",
                    "summary_pass": "Test expression successfully retrieved",
                    "summary_fail": "Test expression NOT retrieved",
                    "summary_skip": "'Get Test Expression' skipped",
                    "url": c.EXPRESSION_API + "V_EXPRESSION_ID",
                    "schema_func": sf.schema_require_matching_id,
                    "server_settings_update_func": uf.update_expected_format
                },

                {
                    "name": "Expression Not Found",
                    "description": "request /expressions/:id using an "
                        + "expression id known to not exist. Checks content "
                        + "type and status code (4xx). validates response body "
                        + "matches Error schema.",
                    "summary_pass": "Server sends correct response when "
                        + "requested expression not found",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when requested expression not found",
                    "summary_skip": "'Expression Not Found' skipped",
                    "url": c.EXPRESSION_API + c.NONEXISTENT_ID,
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
                }
            ]
        },
    
        "content": {
            "global_properties": {
                "function": cf.expression_get_case,
                "tempfile": "expression_get_content_test.loom",
                "url": c.EXPRESSION_API + "V_EXPRESSION_ID",
                "description": "Asserts correct content of expression "
                    + "matrix columns/rows",
                "summary_pass": "Expression matrix content matches expected",
                "summary_fail": "Expression matrix content DOES NOT match "
                    + "expected",
                "summary_skip": "'Expression Get Content' skipped",
                "download_url": lambda response: response.json()["url"]
            },
            "cases": [
                {
                    "name": "Expression Get Content 1",
                    "i": {
                        "r": 38,
                        "c": 8
                    },
                    "o": {
                        "GeneID": "ENSG00000206549",
                        "GeneName": "PRSS50",
                        "Condition": "bladder transitional cell carcinoma",
                        "Tissue": "urinary bladder",
                        "Sample": "DO472 - primary tumour",
                        "Value": 0.0
                    }
                },
                {
                    "name": "Expression Get Content 2",
                    "i": {
                        "r": 68,
                        "c": 15
                    },
                    "o": {
                        "GeneID": "ENSG00000239589",
                        "GeneName": "LINC00879",
                        "Condition": "breast adenocarcinoma",
                        "Tissue": "breast",
                        "Sample": "DO44273 - primary tumour",
                        "Value": 0.0
                    }
                },
                {
                    "name": "Expression Get Content 3",
                    "i": {
                        "r": 47,
                        "c": 70
                    },
                    "o": {
                        "GeneID": "ENSG00000223273",
                        "GeneName": "RN7SKP172",
                        "Condition": "melanoma",
                        "Tissue": "skin",
                        "Sample": "DO37946 - metastatic tumour",
                        "Value": 0.0
                    }
                },
                {
                    "name": "Expression Get Content 4",
                    "i": {
                        "r": 3,
                        "c": 38
                    },
                    "o": {
                        "GeneID": "ENSG00000084693",
                        "GeneName": "AGBL5",
                        "Condition": "endometrial adenocarcinoma",
                        "Tissue": "uterus",
                        "Sample": "DO43811 - primary tumour",
                        "Value": 50.0
                    }
                },
                {
                    "name": "Expression Get Content 5",
                    "i": {
                        "r": 30,
                        "c": 92
                    },
                    "o": {
                        "GeneID": "ENSG00000186501",
                        "GeneName": "TMEM222",
                        "Condition": "renal cell carcinoma",
                        "Tissue": "kidney",
                        "Sample": "DO46856 - normal",
                        "Value": 16.0
                    }
                },
                {
                    "name": "Expression Get Content 6",
                    "i": {
                        "r": 83,
                        "c": 74
                    },
                    "o": {
                        "GeneID": "ENSG00000255543",
                        "GeneName": "AP005597.4",
                        "Condition": "ovarian adenocarcinoma",
                        "Tissue": "ovary",
                        "Sample": "DO46366 - primary tumour",
                        "Value": 0.0
                    }
                },
                {
                    "name": "Expression Get Content 7",
                    "i": {
                        "r": 52,
                        "c": 9
                    },
                    "o": {
                        "GeneID": "ENSG00000227172",
                        "GeneName": "AC011290.1",
                        "Condition": "bladder transitional cell carcinoma",
                        "Tissue": "urinary bladder",
                        "Sample": "DO561 - primary tumour",
                        "Value": 0.7
                    }
                },
                {
                    "name": "Expression Get Content 8",
                    "i": {
                        "r": 31,
                        "c": 89
                    },
                    "o": {
                        "GeneID": "ENSG00000188763",
                        "GeneName": "FZD9",
                        "Condition": "renal cell carcinoma",
                        "Tissue": "kidney",
                        "Sample": "DO20604 - primary tumour",
                        "Value": 0.4
                    }
                },
                {
                    "name": "Expression Get Content 9",
                    "i": {
                        "r": 82,
                        "c": 13
                    },
                    "o": {
                        "GeneID": "ENSG00000254946",
                        "GeneName": "AC073172.2",
                        "Condition": "breast adenocarcinoma",
                        "Tissue": "breast",
                        "Sample": "DO2995 - primary tumour",
                        "Value": 0.0
                    }
                },
                {
                    "name": "Expression Get Content 10",
                    "i": {
                        "r": 95,
                        "c": 93
                    },
                    "o": {
                        "GeneID": "ENSG00000266172",
                        "GeneName": "ENSG00000266172",
                        "Condition": "renal cell carcinoma",
                        "Tissue": "kidney",
                        "Sample": "DO46909 - primary tumour",
                        "Value": 0.0
                    }
                }
            ]
        }
    }, "expression_formats": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION FORMATS
        # # # # # # # # # # # # # # # # # # # # 
        "name": "expression_formats",
        "description": "Requests the /expressions/formats endpoint",
        "pass_text": "'Expression Formats' endpoint correctly implemented",
        "fail_text": "'Expression Formats' endpoint NOT correctly implemented",
        "skip_text": "'Expression formats' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "url": c.EXPRESSION_API + "formats",
                "schema_file": c.SCHEMA_FILE_STRING_ARRAY,
            },

            "cases": [
                {
                    "name": "Get Supported Expression Formats",
                    "description": "request /expressions/formats. checks "
                        + "content type and status code (200). validates "
                        + "response body is an array of strings.",
                    "summary_pass": "Expression formats successfully retrieved",
                    "summary_fail": "Expression formats NOT retrieved",
                    "summary_skip": "'Get Supported Expression Formats' "
                        + "skipped",
                }
            ]
        }
    }, "expression_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_filters",
        "description": "Requests the /expressions/search/filters endpoint.",
        "pass_text": "'Expression Search Filters' endpoint correctly "
            + "implemented",
        "fail_text": "'Expression Search Filters' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Expression Search Filters' test skipped",

        "api": {
            "global_properties": {
                "url": c.EXPRESSION_API + "search/filters",
                "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
                "http_method": c.HTTP_GET,
                "request_params": {},
                "server_settings_update_func": uf.update_supported_filters
            },

            "cases": [
                {
                    "name": "Expression Search Filters",
                    "description": "request /expressions/search/filters. "
                        + "checks content type and status code (200). "
                        + "validates response body matches search "
                        + "filter array schema.",
                    "summary_pass": "Expression search filters successfully "
                        + "retrieved",
                    "summary_fail": "Expression search filters NOT retrieved",
                    "summary_skip": "'Expression Search Filters' skipped",
                }
            ]
        }
    }, "expression_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search",
        "description": "Requests the /expressions/search endpoint.",
        "pass_text": "'Expression Search' endpoint correctly implemented",
        "fail_text": "'Expression Search' endpoint NOT correctly implemented",
        "skip_text": "'Expression Search' test skipped",

        "api": {
            "global_properties": {
                "url": c.EXPRESSION_API + "search",
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Search Expressions by Format",
                    "description": "requests /expressions/search, only "
                       + "specifying the required 'format' parameter. checks "
                       + "content type and status code (200). validates "
                       + "response body matches expression array schema",
                    "summary_pass": "Expressions can be searched by format",
                    "summary_fail": "Expressions CANNOT be searched by format",
                    "summary_skip": "'Search Expressions by Format' skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Search Expressions With All Filters",
                    "description": "request /expressions/search using all "
                        + "server-supported expression filters. checks content "
                        + "type and status code (200). validates response body "
                        + "matches expression array schema.",
                    "summary_pass": "Expressions can be searched with all "
                        + "filters specified",
                    "summary_fail": "Expressions CANNOT be searched with all "
                        + "filters specified",
                    "summary_skip": "'Search Expressions With All Filters' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": \
                     pf.all_supported_filters_and_format_from_retrieved_settings
                },

                {
                    "name": "Search Expressions With Single Filter, 1",
                    "description": "request /expressions/search using the "
                        + "first parameter filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200). validates response body "
                        + "matches expression array schema",
                    "summary_pass": "Expressions can be searched when first "
                        + "filter parameter is supplied",
                    "summary_fail": "Expressions CANNOT be searched when first "
                        + "filter parameter is supplied",
                    "summary_skip": "'Search Expressions With Single Filter, "
                        + "1' skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.first_supported_filter_and_format
                },

                {
                    "name": "Search Expressions With Single Filter, 2",
                    "description": "request /expressions/search using the "
                        + "second parameter filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200). validates response body "
                        + "matches expression array schema",
                    "summary_pass": "Expressions can be searched when second "
                        + "filter parameter is supplied",
                    "summary_fail": "Expressions CANNOT be searched when "
                        + "second filter parameter is supplied",
                    "summary_skip": "'Search Expressions With Single Filter, "
                        + "2' skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.second_supported_filter_and_format
                },

                {
                    "name": "Expression Search Filters Non-Matching Resources",
                    "description": "request /expressions/search using "
                        + "parameter filters that do not apply to any "
                        + "expression. checks content type and status code "
                        + "(200). validates response body is an empty array.",
                    "summary_pass": "Expression search endpoint filters "
                        + "non-matching resources",
                    "summary_fail": "Expression search endpoint DOES NOT "
                        + "filter non-matching resources",
                    "summary_skip": "'Expression Search Filters Non-Matching "
                        + "Resources' skipped",
                    "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
                    "request_params_func": pf.incorrect_filters_and_format
                },

                {
                    "name": "Expression Search Format Not Specified",
                    "description": "request /expressions/search endpoint "
                        + "without specifying the required 'format' parameter. "
                        + "checks content type and status code (4xx). "
                        + "validates response body is an error message JSON.",
                    "summary_pass": "Server returns error when format not "
                        + "specified",
                    "summary_fail": "Server DOES NOT return error when format "
                        + "not specified",
                    "summary_skip": "'Expression Search Format Not Specified' "
                        + "skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {},
                    "expected_status": [400, 404, 422]
                },

                {
                    "name": "Expression Search Filetypes Match",
                    "description": "request /expressions/search endpoint with "
                        + "'format' parameter specified. checks "
                        + "content type and status code (200). validates "
                        + "expression objects in response body contain a "
                        + "fileType that matches the requested format.",
                    "summary_pass": "Expression fileTypes match requested "
                        + "format",
                    "summary_fail": "Expression fileTypes DO NOT match "
                        + "requested format",
                    "summary_skip": "'Expression Search Filetypes Match' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Expression Search No Filetype Mismatches",
                    "description": "request /expressions/search with "
                        + "'format' parameter that does not match the format "
                        + "of the expression in test dataset. checks content "
                        + "type and status code (200). validates expression "
                        + "objects in response body have a fileType matching "
                        + "the requested format.",
                    "summary_pass": "Expression fileTypes match requested "
                        + "format",
                    "summary_fail": "Expression fileTypes DO NOT match "
                        + "requested format",
                    "summary_skip": "'Expression Search No Filetype "
                        + "Mismatches' skipped",
                    "schema_func": \
                        sf.schema_require_matching_search_params_allow_empty,
                    "request_params_func": pf.switch_format_param
                },
            ]
        },

        "content": {
            "global_properties": {
                "function": cf.expression_search_case,
                "tempfile": "expression_search_content_test.loom",
                "url": c.EXPRESSION_API + "search",
                "description": "Asserts correct slicing/subsetting of "
                    + "expression matrix when slice parameters are passed to "
                    + "search endpoint",
                "summary_pass": "Sliced expression matrix rows, columns, and "
                    + "values match expected",
                "summary_fail": "Sliced expression matrix rows, columns, and "
                    + "values DO NOT match expected",
                "summary_skip": "'Expression Search Slice' skipped",
                "request_params_func": \
                    pf.all_supported_filters_format_and_slice_params,
                "download_url": lambda response: response.json()[0]["url"]
            },
            "cases": [
                {
                    "name": "Slice by featureIDList",
                    "featureIDList": [
                        "ENSG00000037965", "ENSG00000243503", "ENSG00000259285"
                    ],
                },

                {
                    "name": "Slice by featureNameList",
                    "featureNameList": [
                        "PGLYRP3", "PRSS50", "SNRPFP1", "OR5AC4P",
                        "CLIC1", "RF00092", "AC100827.4"
                    ],
                },

                {
                    "name": "Slice by sampleIDList",
                    "sampleIDList": [
                        "DO22935 - primary tumour", "DO20604 - primary tumour",
                        "DO48516 - primary tumour", "DO42881 - primary tumour",
                        "DO6144 - primary tumour", "DO40948 - primary tumour",
                        "DO472 - primary tumour", "DO48505 - primary tumour"
                    ]
                },

                #TODO: restore minExpression/maxExpression test cases
                # {
                #     "name": "Slice by minExpression",
                #     "minExpression": [
                #         {
                #             "threshold": 100,
                #            "featureName": "CLIC1"
                #          },
                #         {
                #             "threshold": 50,
                #             "featureName": "TSPAN6"
                #         },
                #         {
                #             "threshold": 30,
                #             "featureName": "LTV1"
                #         },
                #     ]
                # },
                
                # {
                #     "name": "Slice by maxExpression",
                #     "maxExpression": [
                #         {
                #             "threshold": 500,
                #             "featureName": "CLIC1"
                #         },
                #         {
                #             "threshold": 80,
                #             "featureName": "TSPAN6"
                #         },
                #         {
                #             "threshold": 50,
                #             "featureName": "LTV1"
                #         },
                #         {
                #             "threshold": 50,
                #             "featureName": "TRIM22"
                #         },
                #         {
                #             "threshold": 50,
                #             "featureName": "NCOA5"
                #         }
                #     ]
                # },

                {
                    "name": "slice by featureIDList and sampleIDList",
                    "featureIDList": [
                        "ENSG00000106278", "ENSG00000142025", "ENSG00000171487",
                        "ENSG00000184471", "ENSG00000213719", "ENSG00000239589"
                    ],
                    "sampleIDList": [
                        "DO52655 - primary tumour", "DO52685 - primary tumour",
                        "DO25887 - primary tumour",
                    ]
                },

                {
                    "name": "slice by featureNameList and sampleIDList",
                    "featureNameList": [
                        "SH3BP1", "APOL5", "RN7SL592P"
                    ],
                    "sampleIDList": [
                        "DO1249 - primary tumour", "DO28763 - primary tumour", 
                        "DO33408 - primary tumour", "DO219961 - primary tumour",
                        "DO2995 - primary tumour", "DO18671 - primary tumour",
                        "DO219106 - primary tumour"
                    ]
                },

                #TODO: restore minExpression/maxExpression test cases
                # {
                #     "name": "slice by featureIDList, sampleIDList, and "
                #         + "minExpression",
                #     "featureIDList": [
                #         "ENSG00000110876", "ENSG00000145740", "ENSG00000106278",
                #         "ENSG00000186501", "ENSG00000198677", "ENSG00000124160",
                #         "ENSG00000132274", "ENSG00000135521", "ENSG00000000003",
                #         "ENSG00000213719"
                #     ],
                #     "sampleIDList": [
                #         'DO472 - primary tumour', 'DO1954 - primary tumour',
                #         'DO2503 - primary tumour', 'DO220478 - normal',
                #         'DO219106 - primary tumour', 'DO37259 - primary tumour',
                #         'DO9042 - primary tumour', 'DO40948 - primary tumour',
                #         'DO42881 - primary tumour', 'DO43811 - primary tumour'
                #     ],
                #     "minExpression": [
                #         {
                #             "threshold": 400,
                #             "featureName": "CLIC1"
                #         },
                #         {
                #             "threshold": 140,
                #             "featureName": "TSPAN6"
                #         },
                #         {
                #             "threshold": 35,
                #             "featureName": "LTV1"
                #         },
                #     ]
                # },

                # {
                #     "name": "slice by featureIDList, sampleIDList, and "
                #         + "maxExpression",
                #     "featureIDList": [
                #         "ENSG00000110876", "ENSG00000145740", "ENSG00000106278",
                #         "ENSG00000186501", "ENSG00000198677", "ENSG00000124160",
                #         "ENSG00000132274", "ENSG00000135521", "ENSG00000000003",
                #         "ENSG00000213719"
                #     ],
                #     "sampleIDList": [
                #         'DO45161 - primary tumour', 'DO45217 - primary tumour',
                #         'DO28763 - primary tumour', 'DO46342 - primary tumour',
                #         'DO46366 - primary tumour', 'DO46380 - primary tumour',
                #         'DO46408 - primary tumour', 
                #         'DO46556 - recurrent tumour', 
                #         'DO46597 - primary tumour', 'DO34608 - primary tumour'
                #     ],
                #     "maxExpression": [
                #         {
                #             "threshold": 1500,
                #             "featureName": "CLIC1"
                #         },
                #         {
                #             "threshold": 450,
                #             "featureName": "TSPAN6"
                #         },
                #         {
                #             "threshold": 300,
                #             "featureName": "LTV1"
                #         },
                #     ]
                # },

                # {
                #     "name": "slice by featureIDList, sampleIDList, "
                #         + "minExpression, and maxExpression",
                #     "featureIDList": [
                #         "ENSG00000110876", "ENSG00000145740", "ENSG00000106278",
                #         "ENSG00000186501", "ENSG00000198677", "ENSG00000124160",
                #         "ENSG00000132274", "ENSG00000135521", "ENSG00000000003",
                #         "ENSG00000213719"
                #     ],
                #     "sampleIDList": [
                #         'DO45161 - primary tumour', 'DO45217 - primary tumour',
                #         'DO28763 - primary tumour', 'DO46342 - primary tumour',
                #         'DO46366 - primary tumour', 'DO46380 - primary tumour',
                #         'DO46408 - primary tumour', 
                #         'DO46556 - recurrent tumour', 
                #         'DO46597 - primary tumour', 'DO34608 - primary tumour'
                #     ],
                #     "minExpression": [
                #         {
                #             "threshold": 400,
                #             "featureName": "CLIC1"
                #         },
                #         {
                #             "threshold": 140,
                #             "featureName": "TSPAN6"
                #         },
                #         {
                #             "threshold": 35,
                #             "featureName": "LTV1"
                #         },
                #     ],
                #     "maxExpression": [
                #         {
                #             "threshold": 1500,
                #             "featureName": "CLIC1"
                #         },
                #         {
                #             "threshold": 450,
                #             "featureName": "TSPAN6"
                #         },
                #         {
                #             "threshold": 300,
                #             "featureName": "LTV1"
                #         },
                #     ]
                # }
            ]
        }
    }, "expression_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "expression_endpoint_not_implemented",
        "description": "Requests various /expressions routes, expecting the "
                       + "service to respond with a 'Not Implemented' status "
                       + "code",
        "pass_text": "Expression endpoints correctly non-implemented",
        "fail_text": "Expression endpoints NOT correctly non-implemented",
        "skip_text": "Expression endpoints not implemented test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {},
                "expected_status": [501],
                "schema_file": c.SCHEMA_FILE_EMPTY
            },

            "cases": [
                {
                    "name": "Expression Get Not Implemented",
                    "description": "request /expressions/:id, expecting "
                        + "501 status code",
                    "summary_pass": "Expression Get correctly non-implemented",
                    "summary_fail": "Expression Get NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Expression Get Not Implemented' skipped",
                    "url": c.EXPRESSION_API + c.NONEXISTENT_ID
                },

                {
                    "name": "Expression Search Not Implemented",
                    "description": "request /expressions/search, expecting 501 "
                        + "status code",
                    "summary_pass": "Expression Search correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Search NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Expression Search Not Implemented' "
                        + "skipped",
                    "url": c.EXPRESSION_API + "search"
                },

                {
                    "name": "Expression Search Filters Not Implemented",
                    "description": "request /expressions/search/filters, "
                        + "expecting 501 status code",
                    "summary_pass": "Expression Search Filters correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Search Filters NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Expression Search Filters Not "
                        + "Implemented' skipped",
                    "url": c.EXPRESSION_API + "search/filters"
                },

                {
                    "name": "Expression Formats Not Implemented",
                    "description": "request /expressions/formats, "
                        + "expecting 501 status code",
                    "summary_pass": "Expression Formats correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Formats NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Expression Formats Not Implemented' "
                        + "skipped",
                    "url": c.EXPRESSION_API + "formats",
                }
            ]
        }
    }, "continuous_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS GET
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_get",
        "description": "Requests the /continuous/:id endpoint",
        "pass_text": "'Get Continuous by Id' endpoint correctly implemented",
        "fail_text": "'Get Continuous by Id' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Get Continuous by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Continuous",
                    "description": "request /continous/:id using test "
                        + "continuous id. checks content type and status code "
                        + "(200).",
                    "summary_pass": "Test continuous successfully retrieved",
                    "summary_fail": "Test continuous NOT retrieved",
                    "summary_skip": "'Get Test Continuous' skipped",
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID",
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": ["application/vnd.loom", 
                                    "text/tab-separated-values"],
                    "is_json": False
                },

                {
                    "name": "Continuous Not Found",
                    "description": "request /continuous/:id using a " 
                        + "continuous id known to not exist. checks "
                        + "content type and status code (4xx). validates "
                        + "response body matches error schema in the "
                        + "specification",
                    "summary_pass": "Server sends correct response when "
                        + "requested continuous not found",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when requested continuous not found",
                    "summary_skip": "'Continuous Not Found' skipped",
                    "url": c.CONTINUOUS_API + c.NONEXISTENT_ID,
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
                },

                {
                    "name": "Continuous Get Start Specified Without Chr",
                    "description": "request /continuous/:id, specifying start " 
                        + "parameter without chr. checks content type and "
                        + "status code (400). validates response body matches "
                        + "error schema",
                    "request_params": {"start": "5"},
                    "summary_pass": "Server sends correct response when "
                        + "start is specified without chr",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when start is specified without chr",
                    "summary_skip": "'Continuous Get Start Specified Without "
                        + "Chr' skipped",
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "use_default_media_types": True,
                    "media_types": ["application/vnd.loom", 
                                    "text/tab-separated-values"],
                    "expected_status": [400]
                },

                {
                    "name": "Continuous Get End Specified Without Chr",
                    "description": "request /continuous/:id, specifying end " 
                        + "parameter without chr. checks content type and "
                        + "status code (400). validates response body matches "
                        + "error schema",
                    "request_params": {"end": "1000"},
                    "summary_pass": "Server sends correct response when "
                        + "end is specified without chr",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when end is specified without chr",
                    "summary_skip": "'Continuous Get End Specified Without "
                        + "Chr' skipped",
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "use_default_media_types": True,
                    "media_types": ["application/vnd.loom", 
                                    "text/tab-separated-values"],
                    "expected_status": [400]
                },

                {
                    "name": "Continuous Get Start Greater Than End",
                    "description": "request /continuous/:id, specifying chr, " 
                        + "start, and end parameters, but start is greater " 
                        + "than end. checks content type and status code "
                        + "(501). validates response body matches error schema",
                    "request_params": {
                        "chr": "1", "start": "200", "end": "100"
                    },
                    "summary_pass": "Server sends correct response when "
                        + "start is greater than end",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when start is greater than end",
                    "summary_skip": "'Continuous Get Start Greater Than End' "
                        + "skipped",
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "use_default_media_types": True,
                    "media_types": ["application/vnd.loom", 
                                    "text/tab-separated-values"],
                    "expected_status": [501]
                }
            ]
        },

        "content": {
            "global_properties": {
                "function": cf.continuous_get_case,
                "tempfile": "continuous_get_content_test.loom",
                "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID",
                "download_url": lambda response: response.url,
                "request_params_func": \
                    pf.chr_start_end,
                "summary_pass": "Continuous matrix content matches expected",
                "summary_fail": "Continuous matrix content DOES NOT match "
                    + "expected",
                "summary_skip": "'Continuous Get Content' test case skipped",
            },

            "cases": [

                # Value assertion case 1
                {
                    "name": "Continuous Get Content, Assert Correct Values, 1",
                    "description": "Assert continuous rows, columns, and cell "
                        + "values match expected",
                    "assert_values": [
                        {
                            "i": { # input to assertion function,
                                   # ie attribute values from downloaded matrix
                                "r": 1, # row
                                "c": 20 # col
                            },
                            "o": { # output, or expected values
                                "Track": "61729_test", # expected val at row 1
                                "Position": "chr1:20",
                                "Value": 8.904
                            }
                        },

                        {
                            "i": {
                                "r": 0,
                                "c": 5
                            },
                            "o": {
                                "Track": "61721_test",
                                "Position": "chr1:5",
                                "Value": 6.205
                            } 
                        },

                        {
                            "i": {
                                "r": 2,
                                "c": 212
                            },
                            "o": {
                                "Track": "61733_test",
                                "Position": "chr5:143",
                                "Value": 8.779
                            } 
                        },

                        {
                            "i": {
                                "r": 3,
                                "c": 159
                            },
                            "o": {
                                "Track": "61737_test",
                                "Position": "chr5:90",
                                "Value": 24.704
                            } 
                        },

                        {
                            "i": {
                                "r": 1,
                                "c": 66
                            },
                            "o": {
                                "Track": "61729_test",
                                "Position": "chr1:66",
                                "Value": 6.975
                            } 
                        }
                    ]
                },

                # Chromosome assertion cases 1 and 2
                {
                    "name": "Continuous Get Content, chr, 1",
                    "description": "Assert positions in continuous matrix "
                        + "are all of same chromosome as requested",
                    "chr": "chr1"
                },

                {
                    "name": "Continuous Get Content, chr, 2",
                    "description": "Assert positions in continuous matrix "
                        + "are all of same chromosome as requested",
                    "chr": "chr5"
                },

                # Chromosome and start assertion cases 1 and 2
                {
                    "name": "Continuous Get Content, chr and start, 1",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr1",
                    "start": "32"
                },

                {
                    "name": "Continuous Get Content, chr and start, 2",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr5",
                    "start": "100"
                },

                # Chromosome and end assertion cases 1 and 2
                {
                    "name": "Continuous Get Content, chr and end, 1",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr1",
                    "end": "22"
                },

                {
                    "name": "Continuous Get Content, chr and end, 2",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr5",
                    "end": "49"
                },
                
                # Chromosome, start, and end assertion cases 1 and 2
                {
                    "name": "Continuous Get Content, chr, start, and end, 1",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr1",
                    "start": "30",
                    "end": "50"
                },

                {
                    "name": "Continuous Get Content, chr, start, and end, 2",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr5",
                    "start": "69",
                    "end": "117"
                }
            ]
            
        }
    }, "continuous_formats": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS FORMATS
        # # # # # # # # # # # # # # # # # # # # 
        "name": "continuous_formats",
        "description": "Requests the /continuous/formats endpoint",
        "pass_text": "'Continuous Formats' endpoint correctly implemented",
        "fail_text": "'Continuous Formats' endpoint NOT correctly implemented",
        "skip_text": "'Continuous formats' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "url": c.CONTINUOUS_API + "formats",
                "schema_file": c.SCHEMA_FILE_STRING_ARRAY,
            },

            "cases": [
                {
                    "name": "Get Supported Continuous Formats",
                    "description": "request /continuous/formats. checks "
                        + "content type and status code (200). validates "
                        + "response body is an array of strings.",
                    "summary_pass": "Continuous formats successfully retrieved",
                    "summary_fail": "Continuous formats NOT retrieved",
                    "summary_skip": "'Get Supported Continuous Formats' "
                        + "skipped",
                }
            ]
        }
    }, "continuous_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_filters",
        "description": "Requests the /continuous/search/filters endpoint.",
        "pass_text": "'Continuous Search Filters' endpoint correctly "
            + "implemented",
        "fail_text": "'Continuous Search Filters' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Continuous Search Filters' test skipped",

        "api": {
            "global_properties": {
                "url": c.CONTINUOUS_API + "search/filters",
                "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
                "http_method": c.HTTP_GET,
                "request_params": {},
                "server_settings_update_func": uf.update_supported_filters
            },

            "cases": [
                {
                    "name": "Continuous Search Filters",
                    "description": "request /continuous/search/filters. checks "
                                   + "content type and status code (200). "
                                   + "validates response body matches search "
                                   + "filter array schema.",
                    "summary_pass": "Continuous search filters successfully "
                        + "retrieved",
                    "summary_fail": "Continuous search filters NOT retrieved",
                    "summary_skip": "'Continuous Search Filters' skipped",
                }
            ]
        }
    }, "continuous_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search",
        "description": "Requests the /continuous/search endpoint.",
        "pass_text": "'Continuous Search' endpoint correctly implemented",
        "fail_text": "'Continuous Search' endpoint NOT correctly implemented",
        "skip_text": "'Continuous Search' test skipped",

        "api": {
            "global_properties": {
                "url": c.CONTINUOUS_API + "search",
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Search Continuous by Format",
                    "description": "requests /continuous/search, only "
                       + "specifying the required 'format' parameter. checks "
                       + "content type and status code (200). validates "
                       + "response body matches continuous array schema",
                    "summary_pass": "Continuous can be searched by format",
                    "summary_fail": "Continuous CANNOT be searched by format",
                    "summary_skip": "'Search Continuous by Format' skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Search Continuous With All Filters",
                    "description": "request /continuous/search using all "
                        + "server-supported continuous filters. checks content "
                        + "type and status code (200). validates response body "
                        + "matches continuous array schema.",
                    "summary_pass": "Continuous can be searched with all "
                        + "filters specified",
                    "summary_fail": "Continuous CANNOT be searched with all "
                        + "filters specified",
                    "summary_skip": "'Search Continuous With All Filters' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": \
                     pf.all_supported_filters_and_format_from_retrieved_settings
                },

                {
                    "name": "Search Continuous With Single Filter, 1",
                    "description": "request /continuous/search using the first "
                        + "parameter filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200). validates response body "
                        + "matches continuous array schema",
                    "summary_pass": "Continuous can be searched when first "
                        + "filter parameter is supplied",
                    "summary_fail": "Continuous CANNOT be searched when first "
                        + "filter parameter is supplied",
                    "summary_skip": "'Search Continuous With Single Filter, 1' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.first_supported_filter_and_format
                },

                {
                    "name": "Search Continuous With Single Filter, 2",
                    "description": "request /continuous/search using the "
                        + "second parameter filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200). validates response body "
                        + "matches continuous array schema",
                    "summary_pass": "Continuous can be searched when second "
                        + "filter parameter is supplied",
                    "summary_fail": "Continuous CANNOT be searched when second "
                        + "filter parameter is supplied",
                    "summary_skip": "'Search Continuous With Single Filter, 2' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.second_supported_filter_and_format
                },

                {
                    "name": "Continuous Search Filters Non-Matching Resources",
                    "description": "request /continuous/search using "
                        + "parameter filters that do not apply to any "
                        + "continuous. checks content type and status code "
                        + "(200). validates response body is an empty array.",
                    "summary_pass": "Continuous search endpoint filters "
                        + "non-matching resources",
                    "summary_fail": "Continuous search endpoint DOES NOT "
                        + "filter non-matching resources",
                    "summary_skip": "'Continuous Search Filters Non-Matching "
                        + "Resources' skipped",
                    "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
                    "request_params_func": pf.incorrect_filters_and_format
                },

                {
                    "name": "Continuous Search Format Not Specified",
                    "description": "request /continuous/search endpoint "
                        + "without specifying the required 'format' parameter. "
                        + "checks content type and status code (4xx). "
                        + "validates response body is an error message JSON.",
                    "summary_pass": "Server returns error when format not "
                        + "specified",
                    "summary_fail": "Server DOES NOT return error when format "
                        + "not specified",
                    "summary_skip": "'Continuous Search Format Not Specified' "
                        + "skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {},
                    "expected_status": [400, 404, 422]
                },

                {
                    "name": "Continuous Search Filetypes Match",
                    "description": "request /continuous/search endpoint with "
                        + "'format' parameter specified. checks "
                        + "content type and status code (200). validates "
                        + "continuous objects in response body contain a "
                        + "fileType that matches the requested format.",
                    "summary_pass": "Continuous fileTypes match requested "
                        + "format",
                    "summary_fail": "Continuous fileTypes DO NOT match "
                        + "requested format",
                    "summary_skip": "'Continuous Search Filetypes Match' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Continuous Search No Filetype Mismatches",
                    "description": "request /continuous/search with "
                        + "'format' parameter that does not match the format "
                        + "of the continuous in test dataset. checks content "
                        + "type and status code (200). validates continuous "
                        + "objects in response body have a fileType matching "
                        + "the requested format.",
                    "summary_pass": "Continuous fileTypes match requested "
                        + "format",
                    "summary_fail": "Continuous fileTypes DO NOT match "
                        + "requested format",
                    "summary_skip": "'Continuous Search No Filetype "
                        + "Mismatches' skipped",
                    "schema_func": \
                        sf.schema_require_matching_search_params_allow_empty,
                    "request_params_func": pf.switch_format_param
                },

                {
                    "name": "Continuous Search Start Specified Without Chr",
                    "description": "request /continuous/search, specifying " 
                        + "start parameter without chr. checks content type "
                        + "and status code (400). validates response body "
                        + "matches error schema",
                    "summary_pass": "Server sends correct response when "
                        + "start is specified without chr",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when start is specified without chr",
                    "summary_skip": "'Continuous Get Start Specified Without "
                        + "Chr' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {"start": "5"},
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "expected_status": [400]
                },

                {
                    "name": "Continuous Search End Specified Without Chr",
                    "description": "request /continuous/search, specifying end " 
                        + "parameter without chr. checks content type and "
                        + "status code (400). validates response body matches "
                        + "error schema",
                    "summary_pass": "Server sends correct response when "
                        + "end is specified without chr",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when end is specified without chr",
                    "summary_skip": "'Continuous Get End Specified Without "
                        + "Chr' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {"end": "1000"},
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "expected_status": [400]
                },

                {
                    "name": "Continuous Search Start Greater Than End",
                    "description": "request /continuous/search, specifying " 
                        + "chr, start, and end parameters, but start is " 
                        + "greater than end. checks content type and status "
                        + "code (501). validates response body matches error "
                        + "schema",
                    "summary_pass": "Server sends correct response when "
                        + "start is greater than end",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when start is greater than end",
                    "summary_skip": "'Continuous Get Start Greater Than End' "
                        + "skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {
                        "chr": "1", "start": "200", "end": "100"
                    },
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "expected_status": [501]
                }
            ]
        },

        "content": {
            "global_properties": {
                "function": cf.continuous_get_case,
                "tempfile": "continuous_search_content_test.loom",
                "url": c.CONTINUOUS_API + "search",
                "download_url": lambda response: response.json()[0]["url"],
                "request_params_func": \
                    pf.all_supported_filters_format_chr_start_end,
                "description": "Asserts correct subsetting of continuous"
                    + "matrix when parameters (chr, start, end) are passed to "
                    + "search endpoint",
                "summary_pass": "Continuous matrix tracks, positions, and "
                    + "values match expected",
                "summary_fail": "Continuous matrix tracks, positions and "
                    + "values DO NOT match expected",
                "summary_skip": "'Continuous Search Content' test case skipped",
            },

            "cases": [

                # Chromosome assertion cases 1 and 2
                {
                    "name": "Continuous Search Content, chr, 1",
                    "description": "Assert positions in continuous matrix "
                        + "are all of same chromosome as requested",
                    "chr": "chr1"
                },

                {
                    "name": "Continuous Search Content, chr, 2",
                    "description": "Assert positions in continuous matrix "
                        + "are all of same chromosome as requested",
                    "chr": "chr5"
                },

                # Chromosome and start assertion cases 1 and 2
                {
                    "name": "Continuous Search Content, chr and start, 1",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr1",
                    "start": "55"
                },

                {
                    "name": "Continuous Search Content, chr and start, 2",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr5",
                    "start": "16"
                },

                # Chromosome and end assertion cases 1 and 2
                {
                    "name": "Continuous Search Content, chr and end, 1",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr1",
                    "end": "41"
                },

                {
                    "name": "Continuous Search Content, chr and end, 2",
                    "description": "Assert positions in continuous matrix "
                        + "are within specified range",
                    "chr": "chr5",
                    "end": "73"
                },

                # Chromosome, start, and end assertion cases 1 and 2
                {
                    "name": "Continuous Search Content, chr, start, and end, 1",
                    "description": "Assert positions in continuous matrix are "
                        + "within specified range",
                    "chr": "chr1",
                    "start": "51",
                    "end": "66"
                },

                {
                    "name": "Continuous Search Content, chr, start, and end, 2",
                    "description": "Assert positions in continuous matrix are "
                        + "within specified range",
                    "chr": "chr5",
                    "start": "102",
                    "end": "115"
                }
            ]
        }
    }, "continuous_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "continuous_endpoint_not_implemented",
        "description": "Requests various /continuous routes, expecting the "
                       + "service to respond with a 'Not Implemented' status "
                       + "code",
        "pass_text": "Continuous endpoints correctly non-implemented",
        "fail_text": "Continuous endpoints NOT correctly non-implemented",
        "skip_text": "Continuous endpoints not implemented test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {},
                "expected_status": [501],
                "schema_file": c.SCHEMA_FILE_EMPTY
            },

            "cases": [
                {
                    "name": "Continuous Get Not Implemented",
                    "description": "request /continuous/:id, expecting "
                        + "501 status code",
                    "summary_pass": "Continuous Get correctly non-implemented",
                    "summary_fail": "Continuous Get NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Continuous Get Not Implemented' skipped",
                    "url": c.CONTINUOUS_API + c.NONEXISTENT_ID
                },

                {
                    "name": "Continuous Search Not Implemented",
                    "description": "request /continuous/search, expecting 501 "
                        + "status code",
                    "summary_pass": "Continuous Search correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Search NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Continuous Search Not Implemented' "
                        + "skipped",
                    "url": c.CONTINUOUS_API + "search"
                },

                {
                    "name": "Continuous Search Filters Not Implemented",
                    "description": "request /continuous/search/filters, "
                        + "expecting 501 status code",
                    "summary_pass": "Continuous Search Filters correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Search Filters NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Continuous Search Filters Not "
                        + "Implemented' skipped",
                    "url": c.CONTINUOUS_API + "search/filters"
                },

                {
                    "name": "Continuous Formats Not Implemented",
                    "description": "request /continuous/formats, "
                        + "expecting 501 status code",
                    "summary_pass": "Continuous Formats correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Formats NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Continuous Formats Not Implemented' "
                        + "skipped",
                    "url": c.CONTINUOUS_API + "formats",
                }
            ]
        }
    }
}
"""dict: dictionary of dicts, each representing a test scenario"""


TESTS_BY_OBJECT_TYPE = {
    "projects": [
        "project_get",
        "project_search_filters",
        "project_search"
        
    ],
    "studies": [
        "study_get",
        "study_search_filters",
        "study_search"
    ],
    "expressions": [
        "expression_get",
        "expression_formats",
        "expression_search_filters",
        "expression_search"
    ],
    "continuous": [
        "continuous_get",
        "continuous_formats",
        "continuous_search_filters",
        "continuous_search"
    ]
}
"""dict: names of tests by project, study, expression object types"""

NOT_IMPLEMENTED_TESTS_BY_OBJECT_TYPE = {
    "projects": [
        "project_endpoint_not_implemented"
    ],
    "studies": [
        "study_endpoint_not_implemented"
    ],
    "expressions": [
        "expression_endpoint_not_implemented"
    ],
    "continuous": [
        "continuous_endpoint_not_implemented"
    ]
}
"""dict: names of tests by endpoint obj types, when endpoint not implemented"""
