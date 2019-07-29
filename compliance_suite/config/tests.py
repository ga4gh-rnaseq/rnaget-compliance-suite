# -*- coding: utf-8 -*-
"""Module compliance_suite.config.tests.py

This module contains all test scenarios as a dict of dicts. Each dict contains
specifications for a single test scenario. Each dict serves as input to a
compliance_suite.tests.Test instance constructor.
This module also contains the names of each test, grouped by the object type
they pertain to (project, study, expression).

Attributes:
    TESTS_DICT (dict): attributes for all test scenarios as a dict of dicts.
        Each sub-dict contains attributes for a single test:
        name (required): unique name describing the test
        uri (required): URI that request will be sent to (excluding base url)
        http_method (required): specify get or post request
        pass_text (required): message to display if test is passed
        fail_text (required): message to display if test is failed
        skip_text (required): message to display if test is skipped

        Either of the following:
            schema_file: JSON schema that the response should match
            schema_func: function that returns the correct schema file based on
                the value of request parameters
        
        apply_params (required): "all" if all param filters applied at once,
            "cases" if param filters tested one at a time, "no" if params not
            applied at all, "some" if a specified list of params to use is
            supplied
        
        if apply_params == "some", specified_params is required,
        if apply_params == "cases", specified_params is optional,
        if apply_params is anything else, specified_params is not included
            specified_params: if 'apply_params' is 'some,' then this list 
                includes the specific parameters to supply for the test. If
                'apply_params' is 'cases', then this list includes parameters
                that will be always supplied for each case in the test scenario

        replace_params (optional): bool indicating whether to replace request
            params from the yaml file with something else

        If replace_params == True, either param_replacement or param_func
        is required
            param_replacement: str, if replace_params is true, indicate what to
                replace ALL request params with
            param_func: function, if replace_params is true, indicate a function
                that modifies the parameters

        use_default_media_types (optional): bool indicating whether to 
            include default json media types in the test request accept header
            (true by default)
        
        if use_default_media_types == False, media_types is required,
        if use_default_media_types == True, media_types is optional
            media_types (optional): list indicating test-specific
                accepted media types (to be used instead of or in addition to 
                defaults)
        
        expected_status (optional): list of ints indicating expected response
            codes. If nothing specified, test expects only OK status code (200)
        is_json (optional): boolean indicating if response body is in JSON.
            True by default if not specified.
    
    TESTS_BY_OBJECT_TYPE (dict): lists the name of tests grouped by the object
        type they pertain to (project, study, expression)
    
    NOT_IMPLEMENTED_TESTS_BY_OBJECT_TYPE (dict): lists the name of tests
        associated with non-implemented endpoints, grouped by the object type
        they pertain to. Non-implemented endpoints must still be correctly
        configured, ie must yield 501 response.
"""

import compliance_suite.config.constants as c
import compliance_suite.config.schema_functions as sf
import compliance_suite.config.param_functions as pf
import compliance_suite.config.content_test_functions as cf
import compliance_suite.config.functions.update_server_settings as uf

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
                    "description": "request /projects/:id using test project id. "
                                + "checks content type and status code (200). "
                                + "validates response body matches Project "
                                + "object schema.",
                    "summary_pass": "Test project successfully retrieved",
                    "summary_fail": "Test project NOT retrieved",
                    "summary_skip": "'Get Test Project' skipped",
                    "url": c.PROJECT_API + "V_PROJECT_ID",
                    "schema_file": c.SCHEMA_FILE_PROJECT
                },

                {
                    "name": "Project Not Found",
                    "description": "request /projects/:id using a project id known "
                        + "to not exist. Checks content type and status code "
                        + "(4xx). Validates response body matches Error schema.",
                    "summary_pass": "Server sends correct response when requested project not found",
                    "summary_fail": "Server DOES NOT send correct response when requested project not found",
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
        "fail_text": "'Project Search Filters' endpoint NOT correctly implemented",
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
                    "summary_pass": "Project search filters successfully retrieved",
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
                    "summary_fail": "Projects CANNOT be searched without filters",
                    "summary_skip": "'Search Projects Without Filters' skipped",
                    "schema_file": c.SCHEMA_FILE_PROJECT_ARRAY_FULL,
                    "request_params": {}
                },

                {
                    "name": "Search Projects With All Filters",
                    "description": "request /projects/search using all "
                       + "server-supported project filters. checks content "
                       + "type and status code (200). validates response body "
                       + "matches project array schema.",
                    "summary_pass": "Projects can be searched with all filters specified",
                    "summary_fail": "Projects CANNOT be searched with all filters specified",
                    "summary_skip": "'Search Projects With All Filters' skipped",
                    "schema_file": c.SCHEMA_FILE_PROJECT_ARRAY_FULL,
                    "request_params_func": pf.all_supported_filters
                },

                {
                    "name": "Search Projects With Single Filter, 1",
                    "description": "request /projects/search using the first "
                       + "parameter filter supported by server. checks "
                       + "type and status code (200). validates response body "
                       + "matches project array schema",
                    "summary_pass": "Projects can be searched when first filter parameter is supplied",
                    "summary_fail": "Projects CANNOT be searched when first filter parameter is supplied",
                    "summary_skip": "'Search Projects With Single Filter, 1' skipped",
                    "schema_file": c.SCHEMA_FILE_PROJECT_ARRAY_FULL,
                    "request_params_func": pf.first_supported_filter
                },

                {
                    "name": "Search Projects With Single Filter, 2",
                    "description": "request /projects/search using the second "
                       + "parameter filter supported by server. checks "
                       + "type and status code (200). validates response body "
                       + "matches project array schema",
                    "summary_pass": "Projects can be searched when second filter parameter is supplied",
                    "summary_fail": "Projects CANNOT be searched when second filter parameter is supplied",
                    "summary_skip": "'Search Projects With Single Filter, 2' skipped",
                    "schema_file": c.SCHEMA_FILE_PROJECT_ARRAY_FULL,
                    "request_params_func": pf.second_supported_filter
                },

                {
                    "name": "Project Search Filters Non-Matching Resources",
                    "description": "request /projects/search using filters "
                       + "that do not apply to any project. "
                       + "checks content type and status code (200). validates "
                       + "response body is an empty array.",
                    "summary_pass": "Project search endpoint filters non-matching resources",
                    "summary_fail": "Project search endpoint DOES NOT filter non-matching resources",
                    "summary_skip": "'Project Search Filters Non-Matching Resources' skipped",
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
                    "summary_fail": "Project Search NOT correctly non-implemented",
                    "summary_skip": "'Project Search Not Implemented' skipped",
                    "url": c.PROJECT_API + "search"
                },

                {
                    "name": "Project Search Filters Not Implemented",
                    "description": "request /projects/search/filters, "
                                   + "expecting 501 status code",
                    "summary_pass": "Project Search Filters correctly non-implemented",
                    "summary_fail": "Project Search Filters NOT correctly non-implemented",
                    "summary_skip": "'Project Search Filters Not Implemented' skipped",
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
                    "schema_file": c.SCHEMA_FILE_STUDY
                },

                {
                    "name": "Study Not Found",
                    "description": "request /studies/:id using a study id known "
                        + "to not exist. Checks content type and status code "
                        + "(4xx). Validates response body matches Error schema.",
                    "summary_pass": "Server sends correct response when requested study not found",
                    "summary_fail": "Server DOES NOT send correct response when requested study not found",
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
        "fail_text": "'Study Search Filters' endpoint NOT correctly implemented",
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
                    "summary_pass": "Study search filters successfully retrieved",
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
                    "summary_fail": "Studies CANNOT be searched without filters",
                    "summary_skip": "'Search Studies Without Filters' skipped",
                    "schema_file": c.SCHEMA_FILE_STUDY_ARRAY_FULL,
                    "request_params": {}
                },

                {
                    "name": "Search Studies With All Filters",
                    "description": "request /studies/search using all "
                       + "server-supported study filters. checks content "
                       + "type and status code (200). validates response body "
                       + "matches study array schema.",
                    "summary_pass": "Studies can be searched with all filters specified",
                    "summary_fail": "Studies CANNOT be searched with all filters specified",
                    "summary_skip": "'Search Studies With All Filters' skipped",
                    "schema_file": c.SCHEMA_FILE_STUDY_ARRAY_FULL,
                    "request_params_func": pf.all_supported_filters
                },

                {
                    "name": "Search Studies With Single Filter, 1",
                    "description": "request /studies/search using the first "
                       + "parameter filter supported by server. checks "
                       + "type and status code (200). validates response body "
                       + "matches study array schema",
                    "summary_pass": "Studies can be searched when first filter parameter is supplied",
                    "summary_fail": "Studies CANNOT be searched when first filter parameter is supplied",
                    "summary_skip": "'Search Studies With Single Filter, 1' skipped",
                    "schema_file": c.SCHEMA_FILE_STUDY_ARRAY_FULL,
                    "request_params_func": pf.first_supported_filter
                },

                {
                    "name": "Search Studies With Single Filter, 2",
                    "description": "request /studies/search using the second "
                       + "parameter filter supported by server. checks "
                       + "type and status code (200). validates response body "
                       + "matches study array schema",
                    "summary_pass": "Studies can be searched when second filter parameter is supplied",
                    "summary_fail": "Studies CANNOT be searched when second filter parameter is supplied",
                    "summary_skip": "'Search Studies With Single Filter, 2' skipped",
                    "schema_file": c.SCHEMA_FILE_STUDY_ARRAY_FULL,
                    "request_params_func": pf.second_supported_filter
                },

                {
                    "name": "Study Search Filters Non-Matching Resources",
                    "description": "request /studies/search using filters "
                       + "that do not apply to any project. "
                       + "checks content type and status code (200). validates "
                       + "response body is an empty array.",
                    "summary_pass": "Study search endpoint filters non-matching resources",
                    "summary_fail": "Study search endpoint DOES NOT filter non-matching resources",
                    "summary_skip": "'Study Search Filters Non-Matching Resources' skipped",
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
                    "summary_fail": "Study Search NOT correctly non-implemented",
                    "summary_skip": "'Study Search Not Implemented' skipped",
                    "url": c.STUDY_API + "search"
                },

                {
                    "name": "Study Search Filters Not Implemented",
                    "description": "request /studies/search/filters, "
                                   + "expecting 501 status code",
                    "summary_pass": "Study Search Filters correctly non-implemented",
                    "summary_fail": "Study Search Filters NOT correctly non-implemented",
                    "summary_skip": "'Study Search Filters Not Implemented' skipped",
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
        "fail_text": "'Get Expression by Id' endpoint NOT correctly implemented",
        "skip_text": "'Get Expression by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Expression",
                    "description": "request /expressions/:id using test expression id. "
                                + "checks content type and status code (200). "
                                + "validates response body matches Expression "
                                + "object schema.",
                    "summary_pass": "Test expression successfully retrieved",
                    "summary_fail": "Test expression NOT retrieved",
                    "summary_skip": "'Get Test Expression' skipped",
                    "url": c.EXPRESSION_API + "V_EXPRESSION_ID",
                    "schema_file": c.SCHEMA_FILE_EXPRESSION,
                    "server_settings_update_func": uf.update_expected_format
                },

                {
                    "name": "Expression Not Found",
                    "description": "request /expressions/:id using an expression id known "
                        + "to not exist. Checks content type and status code "
                        + "(4xx). validates response body matches Error schema.",
                    "summary_pass": "Server sends correct response when requested expression not found",
                    "summary_fail": "Server DOES NOT send correct response when requested expression not found",
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
                "summary_fail": "Expression matrix content DOES NOT match expected",
                "summary_skip": "'Expression Get Content' skipped",
                "download_url": lambda response_json: response_json["URL"]
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
                    "summary_skip": "'Get Supported Expression Formats' skipped",
                }
            ]
        }
    }, "expression_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_filters",
        "description": "Requests the /expressions/search/filters endpoint.",
        "pass_text": "'Expression Search Filters' endpoint correctly implemented",
        "fail_text": "'Expression Search Filters' endpoint NOT correctly implemented",
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
                    "description": "request /expressions/search/filters. checks "
                                   + "content type and status code (200). "
                                   + "validates response body matches search "
                                   + "filter array schema.",
                    "summary_pass": "Expression search filters successfully retrieved",
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
                    "schema_file": c.SCHEMA_FILE_EXPRESSION_ARRAY_FULL,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Search Expressions With All Filters",
                    "description": "request /expressions/search using all "
                       + "server-supported expression filters. checks content "
                       + "type and status code (200). validates response body "
                       + "matches expression array schema.",
                    "summary_pass": "Expressions can be searched with all filters specified",
                    "summary_fail": "Expressions CANNOT be searched with all filters specified",
                    "summary_skip": "'Search Expressions With All Filters' skipped",
                    "schema_file": c.SCHEMA_FILE_EXPRESSION_ARRAY_FULL,
                    "request_params_func": pf.all_supported_filters_and_format_from_retrieved_settings
                },

                {
                    "name": "Search Expressions With Single Filter, 1",
                    "description": "request /expressions/search using the first "
                       + "parameter filter supported by server "
                       + "(in addition to format). checks "
                       + "type and status code (200). validates response body "
                       + "matches expression array schema",
                    "summary_pass": "Expressions can be searched when first filter parameter is supplied",
                    "summary_fail": "Expressions CANNOT be searched when first filter parameter is supplied",
                    "summary_skip": "'Search Expressions With Single Filter, 1' skipped",
                    "schema_file": c.SCHEMA_FILE_EXPRESSION_ARRAY_FULL,
                    "request_params_func": pf.first_supported_filter_and_format
                },

                {
                    "name": "Search Expressions With Single Filter, 2",
                    "description": "request /expressions/search using the second "
                       + "parameter filter supported by server "
                       + "(in addition to format). checks "
                       + "type and status code (200). validates response body "
                       + "matches expression array schema",
                    "summary_pass": "Expressions can be searched when second filter parameter is supplied",
                    "summary_fail": "Expressions CANNOT be searched when second filter parameter is supplied",
                    "summary_skip": "'Search Expressions With Single Filter, 2' skipped",
                    "schema_file": c.SCHEMA_FILE_EXPRESSION_ARRAY_FULL,
                    "request_params_func": pf.second_supported_filter_and_format
                },

                {
                    "name": "Expression Search Filters Non-Matching Resources",
                    "description": "request /expressions/search using "
                       + "parameter filters that do not apply to any "
                       + "expression. checks content type and status code "
                       + "(200). validates response body is an empty array.",
                    "summary_pass": "Expression search endpoint filters non-matching resources",
                    "summary_fail": "Expression search endpoint DOES NOT filter non-matching resources",
                    "summary_skip": "'Expression Search Filters Non-Matching Resources' skipped",
                    "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
                    "request_params_func": pf.incorrect_filters_and_format
                },

                {
                    "name": "Expression Search Format Not Specified",
                    "description": "request /expressions/search endpoint without "
                       + "specifying the required 'format' parameter. checks "
                       + "content type and status code (4xx). validates "
                       + "response body is an error message JSON.",
                    "summary_pass": "Server returns error when format not specified",
                    "summary_fail": "Server DOES NOT return error when format not specified",
                    "summary_skip": "'Expression Search Format Not Specified' skipped",
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
                    "summary_pass": "Expression fileTypes match requested format",
                    "summary_fail": "Expression fileTypes DO NOT match requested format",
                    "summary_skip": "'Expression Search Filetypes Match' skipped",
                    "schema_func": sf.schema_expression_search_filetypes_match,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Expression Search No Filetype Mismatches",
                    "description": "request /expressions/search with "
                       + "'format' parameter that does not match the format "
                       + "of the expression in test dataset. checks content type and "
                       + "status code (200). validates expression objects in "
                       + "response body have a fileType matching the requested "
                       + "format.",
                    "summary_pass": "Expression fileTypes match requested format",
                    "summary_fail": "Expression fileTypes DO NOT match requested format",
                    "summary_skip": "'Expression Search No Filetype Mismatches' skipped",
                    "schema_func": sf.schema_expression_search_no_filetype_mismatches,
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
                "summary_pass": "Sliced expression matrix rows, columns, and values match expected",
                "summary_fail": "Sliced expression matrix rows, columns, and values DO NOT match expected",
                "summary_skip": "'Expression Search Slice' skipped",
                "request_params_func": pf.all_supported_filters_format_and_slice_params,
                "download_url": lambda response_json: response_json[0]["URL"]
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

                {
                    "name": "Slice by minExpression",
                    "minExpression": [
                        {
                            "threshold": 50,
                            "featureName": "TSPAN6"
                        },
                        {
                            "threshold": 75,
                            "featureName": "HOXC8"
                        },
                        {
                            "threshold": 100,
                            "featureName": "RAB27A"
                        }
                    ]
                },

                {
                    "name": "Slice by maxExpression",
                    "maxExpression": [
                        {
                            "threshold": 0.1,
                            "featureName": "TSPAN6"
                        },
                        {
                            "threshold": 0.2,
                            "featureName": "AC090453.1"
                        },
                        {
                            "threshold": 0.1,
                            "featureName": "RF00322"
                        },
                        {
                            "threshold": 0.2,
                            "featureName": "HSPE1P5"
                        },
                        {
                            "threshold": 0.1,
                            "featureName": "RN7SL592P"
                        }
                    ]
                },

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

                {
                    "name": "slice by featureIDList, sampleIDList, and minExpression",
                    "featureIDList": ["ENSG00000100092", "ENSG00000000003"],
                    "sampleIDList": [
                        "DO9042 - primary tumour", "DO41951 - primary tumour",
                        "DO40664 - primary tumour", "DO25887 - primary tumour",
                        "DO47132 - primary tumour"
                    ],
                    "minExpression": [
                        {
                            "threshold": 10,
                            "featureName": "SH3BP1"
                        },
                        {
                            "threshold": 100,
                            "featureName": "TSPAN6"
                        }
                    ]
                },

                {
                    "name": "slice by featureIDList, sampleIDList, and maxExpression",
                    "featureIDList": [
                        "ENSG00000000003", "ENSG00000237269", "ENSG00000250286",
                        "ENSG00000255543"
                    ],
                    "sampleIDList": [
                        "DO561 - primary tumour", "DO220525 - primary tumour",
                        "DO38903 - primary tumour", "DO46856 - normal",
                        "DO46961 - normal"
                    ],
                    "maxExpression": [
                        {
                            "threshold": 0.1,
                            "featureName": "TSPAN6"
                        },
                        {
                            "threshold": 0.2,
                            "featureName": "RBMY2TP"
                        },
                        {
                            "threshold": 0.1,
                            "featureName": "AC021491.2"
                        },
                        {
                            "threshold": 0.2,
                            "featureName": "AP005597.4"
                        }
                    ]
                },

                {
                    "name": "slice by featureIDList, sampleIDList, minExpression, and maxExpression",
                    "featureIDList": [
                        "ENSG00000000003", "ENSG00000201184", "ENSG00000238013",
                        "ENSG00000248585", "ENSG00000251090"
                    ],
                    "sampleIDList": [
                        "DO2995 - primary tumour", "DO220342 - primary tumour",
                        "DO39841 - primary tumour", "DO12352 - primary tumour",
                        "DO15503 - primary tumour"
                    ],
                    "minExpression": [
                        {
                            "threshold": 10,
                            "featureName": "TSPAN6"
                        },
                        {
                            "threshold": 5,
                            "featureName": "RNU4-68P"
                        },
                        {
                            "threshold": 10,
                            "featureName": "AC109583.1"
                        },
                        {
                            "threshold": 5,
                            "featureName": "AC084024.2"
                        },
                        {
                            "threshold": 10,
                            "featureName": "OR5AC4P"
                        }
                    ],
                    "maxExpression": [
                        {
                            "threshold": 50,
                            "featureName": "TSPAN6"
                        },
                        {
                            "threshold": 100,
                            "featureName": "RNU4-68P"
                        },
                        {
                            "threshold": 50,
                            "featureName": "AC109583.1"
                        },
                        {
                            "threshold": 100,
                            "featureName": "AC084024.2"
                        },
                        {
                            "threshold": 50,
                            "featureName": "OR5AC4P"
                        }
                    ]
                }
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
                    "summary_fail": "Expression Get NOT correctly non-implemented",
                    "summary_skip": "'Expression Get Not Implemented' skipped",
                    "url": c.EXPRESSION_API + c.NONEXISTENT_ID
                },

                {
                    "name": "Expression Search Not Implemented",
                    "description": "request /expressions/search, expecting 501 "
                                   + "status code",
                    "summary_pass": "Expression Search correctly non-implemented",
                    "summary_fail": "Expression Search NOT correctly non-implemented",
                    "summary_skip": "'Expression Search Not Implemented' skipped",
                    "url": c.EXPRESSION_API + "search"
                },

                {
                    "name": "Expression Search Filters Not Implemented",
                    "description": "request /expressions/search/filters, "
                                   + "expecting 501 status code",
                    "summary_pass": "Expression Search Filters correctly non-implemented",
                    "summary_fail": "Expression Search Filters NOT correctly non-implemented",
                    "summary_skip": "'Expression Search Filters Not Implemented' skipped",
                    "url": c.EXPRESSION_API + "search/filters"
                },

                {
                    "name": "Expression Formats Not Implemented",
                    "description": "request /expressions/formats, "
                                   + "expecting 501 status code",
                    "summary_pass": "Expression Formats correctly non-implemented",
                    "summary_fail": "Expression Formats NOT correctly non-implemented",
                    "summary_skip": "'Expression Formats Not Implemented' skipped",
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
        "fail_text": "'Get Continuous by Id' endpoint NOT correctly implemented",
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
                    "summary_pass": "Server sends correct response when requested continuous not found",
                    "summary_fail": "Server DOES NOT send correct response when requested continuous not found",
                    "summary_skip": "'Continuous Not Found' skipped",
                    "url": c.CONTINUOUS_API + c.NONEXISTENT_ID,
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
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
                    "summary_skip": "'Get Supported Continuous Formats' skipped",
                }
            ]
        }
    }, "continuous_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_filters",
        "description": "Requests the /continuous/search/filters endpoint.",
        "pass_text": "'Continuous Search Filters' endpoint correctly implemented",
        "fail_text": "'Continuous Search Filters' endpoint NOT correctly implemented",
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
                    "summary_pass": "Continuous search filters successfully retrieved",
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
                "url": c.EXPRESSION_API + "search",
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
                    "schema_file": c.SCHEMA_FILE_CONTINUOUS_ARRAY_FULL,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Search Continuous With All Filters",
                    "description": "request /continuous/search using all "
                       + "server-supported continuous filters. checks content "
                       + "type and status code (200). validates response body "
                       + "matches continuous array schema.",
                    "summary_pass": "Continuous can be searched with all filters specified",
                    "summary_fail": "Continuous CANNOT be searched with all filters specified",
                    "summary_skip": "'Search Continuous With All Filters' skipped",
                    "schema_file": c.SCHEMA_FILE_CONTINUOUS_ARRAY_FULL,
                    "request_params_func": pf.all_supported_filters_and_format_from_retrieved_settings
                },

                {
                    "name": "Search Continuous With Single Filter, 1",
                    "description": "request /continuous/search using the first "
                       + "parameter filter supported by server "
                       + "(in addition to format). checks "
                       + "type and status code (200). validates response body "
                       + "matches continuous array schema",
                    "summary_pass": "Continuous can be searched when first filter parameter is supplied",
                    "summary_fail": "Continuous CANNOT be searched when first filter parameter is supplied",
                    "summary_skip": "'Search Continuous With Single Filter, 1' skipped",
                    "schema_file": c.SCHEMA_FILE_CONTINUOUS_ARRAY_FULL,
                    "request_params_func": pf.first_supported_filter_and_format
                },

                {
                    "name": "Search Continuous With Single Filter, 2",
                    "description": "request /continuous/search using the second "
                       + "parameter filter supported by server "
                       + "(in addition to format). checks "
                       + "type and status code (200). validates response body "
                       + "matches continuous array schema",
                    "summary_pass": "Continuous can be searched when second filter parameter is supplied",
                    "summary_fail": "Continuous CANNOT be searched when second filter parameter is supplied",
                    "summary_skip": "'Search Continuous With Single Filter, 2' skipped",
                    "schema_file": c.SCHEMA_FILE_CONTINUOUS_ARRAY_FULL,
                    "request_params_func": pf.second_supported_filter_and_format
                },

                {
                    "name": "Continuous Search Filters Non-Matching Resources",
                    "description": "request /continuous/search using "
                       + "parameter filters that do not apply to any "
                       + "continuous. checks content type and status code "
                       + "(200). validates response body is an empty array.",
                    "summary_pass": "Continuous search endpoint filters non-matching resources",
                    "summary_fail": "Continuous search endpoint DOES NOT filter non-matching resources",
                    "summary_skip": "'Continuous Search Filters Non-Matching Resources' skipped",
                    "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
                    "request_params_func": pf.incorrect_filters_and_format
                },

                {
                    "name": "Continuous Search Format Not Specified",
                    "description": "request /continuous/search endpoint without "
                       + "specifying the required 'format' parameter. checks "
                       + "content type and status code (4xx). validates "
                       + "response body is an error message JSON.",
                    "summary_pass": "Server returns error when format not specified",
                    "summary_fail": "Server DOES NOT return error when format not specified",
                    "summary_skip": "'Continuous Search Format Not Specified' skipped",
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
                    "summary_pass": "Continuous fileTypes match requested format",
                    "summary_fail": "Continuous fileTypes DO NOT match requested format",
                    "summary_skip": "'Continuous Search Filetypes Match' skipped",
                    "schema_func": sf.schema_continuous_search_filetypes_match,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Continuous Search No Filetype Mismatches",
                    "description": "request /continuous/search with "
                       + "'format' parameter that does not match the format "
                       + "of the continuous in test dataset. checks content type and "
                       + "status code (200). validates continuous objects in "
                       + "response body have a fileType matching the requested "
                       + "format.",
                    "summary_pass": "Continuous fileTypes match requested format",
                    "summary_fail": "Continuous fileTypes DO NOT match requested format",
                    "summary_skip": "'Continuous Search No Filetype Mismatches' skipped",
                    "schema_func": sf.schema_continuous_search_no_filetype_mismatches,
                    "request_params_func": pf.switch_format_param
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
                    "summary_fail": "Continuous Get NOT correctly non-implemented",
                    "summary_skip": "'Continuous Get Not Implemented' skipped",
                    "url": c.CONTINUOUS_API + c.NONEXISTENT_ID
                },

                {
                    "name": "Continuous Search Not Implemented",
                    "description": "request /continuous/search, expecting 501 "
                                   + "status code",
                    "summary_pass": "Continuous Search correctly non-implemented",
                    "summary_fail": "Continuous Search NOT correctly non-implemented",
                    "summary_skip": "'Continuous Search Not Implemented' skipped",
                    "url": c.CONTINUOUS_API + "search"
                },

                {
                    "name": "Continuous Search Filters Not Implemented",
                    "description": "request /continuous/search/filters, "
                                   + "expecting 501 status code",
                    "summary_pass": "Continuous Search Filters correctly non-implemented",
                    "summary_fail": "Continuous Search Filters NOT correctly non-implemented",
                    "summary_skip": "'Continuous Search Filters Not Implemented' skipped",
                    "url": c.CONTINUOUS_API + "search/filters"
                },

                {
                    "name": "Continuous Formats Not Implemented",
                    "description": "request /continuous/formats, "
                                   + "expecting 501 status code",
                    "summary_pass": "Continuous Formats correctly non-implemented",
                    "summary_fail": "Continuous Formats NOT correctly non-implemented",
                    "summary_skip": "'Continuous Formats Not Implemented' skipped",
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
