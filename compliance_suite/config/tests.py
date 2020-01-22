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
import compliance_suite.config.content_test_instances as cti
import compliance_suite.functions.download_matrix as dm
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
    }, "project_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_filters",
        "description": "requests the /projects/filters endpoint",
        "pass_text": "'Project Filters' endpoint correctly implemented",
        "fail_text": "'Project Filters' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Project Filters' test skipped",

        "api": {
            "global_properties": {
                "url": c.PROJECT_API + "filters",
                "http_method": c.HTTP_GET,
                "request_params": {},
                "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
                "server_settings_update_func": uf.update_supported_filters
            },

            "cases": [
                {
                    "name": "Project Filters",
                    "description": "request /projects/filters. checks "
                        + "content type and status code (200). "
                        + "validates response body matches search "
                        + "filter array schema.",
                    "summary_pass": "Project filters successfully "
                        + "retrieved",
                    "summary_fail": "Project filters NOT retrieved",
                    "summary_skip": "'Project Filters' skipped",
                }
            ]
        }
    }, "project_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search",
        "description": "Requests the /projects endpoint",
        "pass_text": "'Project Search' endpoint correctly implemented",
        "fail_text": "'Project Search' endpoint NOT correctly implemented",
        "skip_text": "'Project Search' test skipped",

        "api": {
            "global_properties": {
                "url": c.PROJECT_API,
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Search Projects Without Filters",
                    "description": "request /projects without any "
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
                    "description": "request /projects using all "
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
                    "description": "request /projects using the first "
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
                    "description": "request /projects using the second "
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
                    "description": "request /projects using filters "
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
                    "description": "request /projects, expecting 501 "
                        + "status code",
                    "summary_pass": "Project Search correctly non-implemented",
                    "summary_fail": "Project Search NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Project Search Not Implemented' skipped",
                    "url": c.PROJECT_API
                },

                {
                    "name": "Project Filters Not Implemented",
                    "description": "request /projects/filters, "
                        + "expecting 501 status code",
                    "summary_pass": "Project Filters correctly "
                        + "non-implemented",
                    "summary_fail": "Project Filters NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Project Filters Not Implemented' "
                        + "skipped",
                    "url": c.PROJECT_API + "filters"
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
    }, "study_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_filters",
        "description": "requests the /studies/filters endpoint",
        "pass_text": "'Study Filters' endpoint correctly implemented",
        "fail_text": "'Study Filters' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Study Filters' test skipped",

        "api": {
            "global_properties": {
                "url": c.STUDY_API + "filters",
                "http_method": c.HTTP_GET,
                "request_params": {},
                "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
                "server_settings_update_func": uf.update_supported_filters
            },

            "cases": [
                {
                    "name": "Study Filters",
                    "description": "request /studies/filters. checks "
                        + "content type and status code (200). "
                        + "validates response body matches search "
                        + "filter array schema.",
                    "summary_pass": "Study filters successfully "
                        + "retrieved",
                    "summary_fail": "Study filters NOT retrieved",
                    "summary_skip": "'Study Filters' skipped",
                }
            ]
        }
    }, "study_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search",
        "description": "Requests the /studies endpoint",
        "pass_text": "'Study Search' endpoint correctly implemented",
        "fail_text": "'Study Search' endpoint NOT correctly implemented",
        "skip_text": "'Study Search' test skipped",

        "api": {
            "global_properties": {
                "url": c.STUDY_API,
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Search Studies Without Filters",
                    "description": "request /studies without any "
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
                    "description": "request /studies using all "
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
                    "description": "request /studies using the first "
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
                    "description": "request /studies using the second "
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
                    "description": "request /studies using filters "
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
                    "description": "request /studies, expecting 501 "
                                   + "status code",
                    "summary_pass": "Study Search correctly non-implemented",
                    "summary_fail": "Study Search NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Study Search Not Implemented' skipped",
                    "url": c.STUDY_API
                },

                {
                    "name": "Study Search Filters Not Implemented",
                    "description": "request /studies/filters, "
                        + "expecting 501 status code",
                    "summary_pass": "Study Search Filters correctly "
                        + "non-implemented",
                    "summary_fail": "Study Search Filters NOT correctly "
                        + "non-implemented",
                    "summary_skip": "'Study Search Filters Not Implemented' "
                        + "skipped",
                    "url": c.STUDY_API + "filters"
                }
            ]
        }
    },

    "expression_formats": {
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
    },

    "expression_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_filters",
        "description": "Requests the /expressions/filters endpoint.",
        "pass_text": "'Expression Filters' endpoint correctly "
            + "implemented",
        "fail_text": "'Expression Filters' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Expression Filters' test skipped",

        "api": {
            "global_properties": {
                "url": c.EXPRESSION_API + "filters",
                "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
                "http_method": c.HTTP_GET,
                "request_params": {},
                "server_settings_update_func": uf.update_supported_filters
            },

            "cases": [
                {
                    "name": "Expression Filters",
                    "description": "request /expressions/filters. "
                        + "checks content type and status code (200). "
                        + "validates response body matches search "
                        + "filter array schema.",
                    "summary_pass": "Expression filters successfully "
                        + "retrieved",
                    "summary_fail": "Expression filters NOT retrieved",
                    "summary_skip": "'Expression Filters' skipped",
                }
            ]
        }
    },
    
    "single_expression_ticket": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: SINGLE EXPRESSION TICKET
        # # # # # # # # # # # # # # # # # # # # 
        "name": "single_expression_ticket",
        "description": "Requests the /expressions/:id/ticket endpoint",
        "pass_text": "'Single Expression Ticket by Id' endpoint correctly "
            + "implemented",
        "fail_text": "'Single Expression Ticket by Id' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Single Expression Ticket by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Expression Ticket",
                    "description": "request /expressions/:id/ticket using "
                        + "test expression id. checks content type and status "
                        + "code (200). validates response body matches Ticket "
                        + "schema.",
                    "summary_pass": "Test expression ticket successfully "
                        + "retrieved",
                    "summary_fail": "Test expression ticket NOT retrieved",
                    "summary_skip": "'Get Test Expression Ticket' skipped",
                    "url": c.EXPRESSION_API + "V_EXPRESSION_ID/ticket",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "server_settings_update_func": uf.update_expected_format
                },

                {
                    "name": "Single Expression Ticket - Not Found",
                    "description": "request /expressions/:id/ticket using an "
                        + "expression id known to not exist. Checks content "
                        + "type and status code (4xx). validates response body "
                        + "matches Error schema.",
                    "summary_pass": "Server sends correct response when "
                        + "requested expression not found",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when requested expression not found",
                    "summary_skip": "'Expression Not Found' skipped",
                    "url": c.EXPRESSION_API + c.NONEXISTENT_ID + "/ticket",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
                }
            ]
        },
    
        "content": {
            "global_properties": {
                "tempfile": "single_expression_ticket_content_test.loom",
                "url": c.EXPRESSION_API + "V_EXPRESSION_ID/ticket",
                "description": "Asserts correct expression values and slicing "
                    + "operations",
                "summary_pass": "Expression matrix content matches expected",
                "summary_fail": "Expression matrix content DOES NOT match "
                    + "expected",
                "summary_skip": "'Expression Content Testing' skipped",
                "download_func": dm.download_from_ticket,
                "request_params_func": \
                    pf.expression_slice_params,
            },
            "cases": [
                dict(cti.EXPRESSION_VALUE_1,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_1["name"]),
                dict(cti.EXPRESSION_VALUE_2,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_2["name"]),
                dict(cti.EXPRESSION_VALUE_3,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_3["name"]),
                dict(cti.EXPRESSION_VALUE_4,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_4["name"]),
                dict(cti.EXPRESSION_VALUE_5,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_5["name"]),
                dict(cti.EXPRESSION_VALUE_6,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_6["name"]),
                dict(cti.EXPRESSION_VALUE_7,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_7["name"]),
                dict(cti.EXPRESSION_VALUE_8,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_8["name"]),
                dict(cti.EXPRESSION_VALUE_9,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_9["name"]),
                dict(cti.EXPRESSION_VALUE_10,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_VALUE_10["name"]),
                dict(cti.EXPRESSION_SLICE_1,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_SLICE_1["name"]),
                dict(cti.EXPRESSION_SLICE_2,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_SLICE_2["name"]),
                dict(cti.EXPRESSION_SLICE_3,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_SLICE_3["name"]),
                dict(cti.EXPRESSION_SLICE_4,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_SLICE_4["name"]),
                dict(cti.EXPRESSION_SLICE_5,
                     name="Single Expression Ticket - "
                     + cti.EXPRESSION_SLICE_5["name"])
            ]
        }
    },

    "single_expression_bytes": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: SINGLE EXPRESSION BYTES
        # # # # # # # # # # # # # # # # # # # # 
        "name": "single_expression_bytes",
        "description": "Requests the /expressions/:id/bytes endpoint",
        "pass_text": "'Single Expression Bytes by Id' endpoint correctly "
            + "implemented",
        "fail_text": "'Single Expression Bytes by Id' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Single Expression Bytes by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Expression Bytes",
                    "description": "request /expressions/:id/bytes using "
                        + "test expression id. checks content type and status "
                        + "code (200).",
                    "summary_pass": "Test expression bytes successfully "
                        + "retrieved",
                    "summary_fail": "Test expression bytes NOT retrieved",
                    "summary_skip": "'Get Test Expression Bytes' skipped",
                    "url": c.EXPRESSION_API + "V_EXPRESSION_ID/bytes",
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ],
                    "is_json": False
                },

                {
                    "name": "Single Expression Bytes - Not Found",
                    "description": "request /expressions/:id/bytes using an "
                        + "expression id known to not exist. Checks content "
                        + "type and status code (4xx). validates response body "
                        + "matches Error schema.",
                    "summary_pass": "Server sends correct response when "
                        + "requested expression not found",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when requested expression not found",
                    "summary_skip": "'Expression Not Found' skipped",
                    "url": c.EXPRESSION_API + c.NONEXISTENT_ID + "/bytes",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
                }
            ]
        },
    
        "content": {
            "global_properties": {
                "tempfile": "single_expression_ticket_content_test.loom",
                "url": c.EXPRESSION_API + "V_EXPRESSION_ID/bytes",
                "description": "Asserts correct expression values and slicing "
                    + "operations",
                "summary_pass": "Expression matrix content matches expected",
                "summary_fail": "Expression matrix content DOES NOT match "
                    + "expected",
                "summary_skip": "'Expression Get Content' skipped",
                "download_func": dm.download_from_bytes,
                "request_params_func": \
                    pf.expression_slice_params,
            },
            "cases": [
                dict(cti.EXPRESSION_VALUE_1,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_1["name"]),
                dict(cti.EXPRESSION_VALUE_2,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_2["name"]),
                dict(cti.EXPRESSION_VALUE_3,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_3["name"]),
                dict(cti.EXPRESSION_VALUE_4,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_4["name"]),
                dict(cti.EXPRESSION_VALUE_5,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_5["name"]),
                dict(cti.EXPRESSION_VALUE_6,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_6["name"]),
                dict(cti.EXPRESSION_VALUE_7,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_7["name"]),
                dict(cti.EXPRESSION_VALUE_8,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_8["name"]),
                dict(cti.EXPRESSION_VALUE_9,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_9["name"]),
                dict(cti.EXPRESSION_VALUE_10,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_VALUE_10["name"]),
                dict(cti.EXPRESSION_SLICE_1,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_SLICE_1["name"]),
                dict(cti.EXPRESSION_SLICE_2,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_SLICE_2["name"]),
                dict(cti.EXPRESSION_SLICE_3,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_SLICE_3["name"]),
                dict(cti.EXPRESSION_SLICE_4,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_SLICE_4["name"]),
                dict(cti.EXPRESSION_SLICE_5,
                     name="Single Expression Bytes - " 
                     + cti.EXPRESSION_SLICE_5["name"])
            ]
        }
    },
    
    "multi_expression_ticket": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: MULTI EXPRESSION TICKET
        # # # # # # # # # # # # # # # # # # # #
        "name": "multi_expression_ticket",
        "description": "Requests the /expressions/ticket endpoint.",
        "pass_text": "'Expression Ticket' endpoint correctly implemented",
        "fail_text": "'Expression Ticket' endpoint NOT correctly implemented",
        "skip_text": "'Expression Ticket' test skipped",

        "api": {
            "global_properties": {
                "url": c.EXPRESSION_API + "ticket",
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Expression Ticket by Format",
                    "description": "requests /expressions/ticket, only "
                       + "specifying the required 'format' parameter. checks "
                       + "content type and status code (200). validates "
                       + "response body matches ticket schema",
                    "summary_pass": "Expression Ticket can be retrieved",
                    "summary_fail": "Expression Ticket CANNOT be retrieved",
                    "summary_skip": "'Expression Ticket by Format' skipped",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Expression Ticket - All Filters",
                    "description": "request /expressions/ticket using all "
                        + "server-supported expression filters. checks content "
                        + "type and status code (200). validates response body "
                        + "matches ticket schema.",
                    "summary_pass": "Expression Ticket retrieved when all "
                        + "filters specified",
                    "summary_fail": "Expression Ticket CANNOT be retrieved "
                        + "when all filters specified",
                    "summary_skip": "'Expression Ticket - All Filters' "
                        + "skipped",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "request_params_func": \
                     pf.all_supported_filters_and_format_from_retrieved_settings
                },

                {
                    "name": "Expression Ticket - Single Filter, 1",
                    "description": "request /expressions/ticket using the "
                        + "first filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200). validates response body "
                        + "matches ticket schema",
                    "summary_pass": "Expression Ticket retrieved when first "
                        + "filter supplied",
                    "summary_fail": "Expression Ticket NOT retrieved when "
                        + "first filter supplied",
                    "summary_skip": "'Expression Ticket - Single Filter, "
                        + "1' skipped",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "request_params_func": pf.first_supported_filter_and_format
                },

                {
                    "name": "Expression Ticket - Single Filter, 2",
                    "description": "request /expressions/ticket using the "
                        + "second filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200). validates response body "
                        + "matches ticket schema",
                    "summary_pass": "Expression Ticket retrieved when second "
                        + "filter supplied",
                    "summary_fail": "Expression Ticket NOT retrieved when "
                        + "second filter supplied",
                    "summary_skip": "'Expression Ticket - Single Filter, "
                        + "2' skipped",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "request_params_func": pf.second_supported_filter_and_format
                },

                {
                    "name": "Expression Ticket - Format Not Specified",
                    "description": "request /expressions/ticket endpoint "
                        + "without specifying the required 'format' parameter. "
                        + "checks content type and status code (4xx). "
                        + "validates response body matches error schema.",
                    "summary_pass": "Server returns error when format not "
                        + "specified",
                    "summary_fail": "Server DOES NOT return error when format "
                        + "not specified",
                    "summary_skip": "'Expression Ticket - Format Not "
                        + "Specified' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {},
                    "expected_status": [400, 404, 422]
                },

                {
                    "name": "Expression Ticket - Filetype Matches",
                    "description": "request /expressions/ticket endpoint with "
                        + "'format' parameter specified. checks "
                        + "content type and status code (200). validates "
                        + "ticket fileType matches requested format.",
                    "summary_pass": "Expression Ticket fileType matches "
                        + "request format",
                    "summary_fail": "Expression Ticket fileType DOES NOT match "
                        + "request format",
                    "summary_skip": "'Expression Ticket - Filetypes Match' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.add_format_from_retrieved_settings
                }
            ]
        },

        "content": {
            "global_properties": {
                "tempfile": "multi_expression_ticket_content_test.loom",
                "url": c.EXPRESSION_API + "ticket",
                "description": "Asserts correct slicing/subsetting of "
                    + "expression matrix when slice parameters are passed to "
                    + "/expressions/ticket",
                "summary_pass": "Sliced expression matrix rows, columns, and "
                    + "values match expected",
                "summary_fail": "Sliced expression matrix rows, columns, and "
                    + "values DO NOT match expected",
                "summary_skip": "'Expression Content Testing' skipped",
                "download_func": dm.download_from_ticket,
                "request_params_func": \
                    pf.all_supported_filters_format_and_slice_params
            },
            "cases": [
                dict(cti.EXPRESSION_VALUE_1,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_VALUE_1["name"]),
                dict(cti.EXPRESSION_VALUE_2,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_VALUE_2["name"]),
                dict(cti.EXPRESSION_VALUE_3,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_VALUE_3["name"]),
                dict(cti.EXPRESSION_VALUE_4,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_VALUE_4["name"]),
                dict(cti.EXPRESSION_VALUE_5,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_VALUE_5["name"]),
                dict(cti.EXPRESSION_SLICE_1,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_SLICE_1["name"]),
                dict(cti.EXPRESSION_SLICE_2,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_SLICE_2["name"]),
                dict(cti.EXPRESSION_SLICE_3,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_SLICE_3["name"]),
                dict(cti.EXPRESSION_SLICE_4,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_SLICE_4["name"]),
                dict(cti.EXPRESSION_SLICE_5,
                     name="Multi Expression Ticket - "
                     + cti.EXPRESSION_SLICE_5["name"])
            ]
        }
    }, 

    "multi_expression_bytes": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: MULTI EXPRESSION BYTES
        # # # # # # # # # # # # # # # # # # # #
        "name": "multi_expression_bytes",
        "description": "Requests the /expressions/bytes endpoint.",
        "pass_text": "'Expression Bytes' endpoint correctly implemented",
        "fail_text": "'Expression Bytes' endpoint NOT correctly implemented",
        "skip_text": "'Expression Bytes' test skipped",

        "api": {
            "global_properties": {
                "url": c.EXPRESSION_API + "bytes",
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Expression Bytes by Format",
                    "description": "requests /expressions/bytes, only "
                       + "specifying the required 'format' parameter. checks "
                       + "content type and status code (200).",
                    "summary_pass": "Expression Bytes can be retrieved",
                    "summary_fail": "Expression Bytes CANNOT be retrieved",
                    "summary_skip": "'Expression Bytes by Format' skipped",
                    "request_params_func": \
                        pf.add_format_from_retrieved_settings,
                    "is_json": False,
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ]
                },

                {
                    "name": "Expression Bytes - All Filters",
                    "description": "request /expressions/bytes using all "
                        + "server-supported expression filters. checks content "
                        + "type and status code (200).",
                    "summary_pass": "Expression Bytes retrieved when all "
                        + "filters specified",
                    "summary_fail": "Expression Bytes CANNOT be retrieved "
                        + "when all filters specified",
                    "summary_skip": "'Expression Bytes - All Filters' "
                        + "skipped",
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "is_json": False,
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ]
                },

                {
                    "name": "Expression Bytes - Single Filter, 1",
                    "description": "request /expressions/bytes using the "
                        + "first filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200).",
                    "summary_pass": "Expression Bytes retrieved when first "
                        + "filter supplied",
                    "summary_fail": "Expression Bytes NOT retrieved when "
                        + "first filter supplied",
                    "summary_skip": "'Expression Bytes - Single Filter, "
                        + "1' skipped",
                    "request_params_func": pf.first_supported_filter_and_format,
                    "is_json": False,
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ]
                },

                {
                    "name": "Expression Bytes - Single Filter, 2",
                    "description": "request /expressions/bytes using the "
                        + "second filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200).",
                    "summary_pass": "Expression Bytes retrieved when second "
                        + "filter supplied",
                    "summary_fail": "Expression Bytes NOT retrieved when "
                        + "second filter supplied",
                    "summary_skip": "'Expression Bytes - Single Filter, "
                        + "2' skipped",
                    "request_params_func": \
                        pf.second_supported_filter_and_format,
                    "is_json": False,
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ]
                },

                {
                    "name": "Expression Bytes - Format Not Specified",
                    "description": "request /expressions/bytes endpoint "
                        + "without specifying the required 'format' parameter. "
                        + "checks content type and status code (4xx). "
                        + "validates response body matches error schema.",
                    "summary_pass": "Server returns error when format not "
                        + "specified",
                    "summary_fail": "Server DOES NOT return error when format "
                        + "not specified",
                    "summary_skip": "'Expression Bytes - Format Not "
                        + "Specified' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {},
                    "expected_status": [400, 404, 422]
                }
            ]
        },

        "content": {
            "global_properties": {
                "tempfile": "multi_expression_bytes_content_test.loom",
                "url": c.EXPRESSION_API + "bytes",
                "description": "Asserts correct slicing/subsetting of "
                    + "expression matrix when slice parameters are passed to "
                    + "endpoint",
                "summary_pass": "Sliced expression matrix rows, columns, and "
                    + "values match expected",
                "summary_fail": "Sliced expression matrix rows, columns, and "
                    + "values DO NOT match expected",
                "summary_skip": "'Expression Content Testing' skipped",
                "download_func": dm.download_from_bytes,
                "request_params_func": \
                    pf.all_supported_filters_format_and_slice_params
            },
            "cases": [
                dict(cti.EXPRESSION_VALUE_6,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_VALUE_6["name"]),
                dict(cti.EXPRESSION_VALUE_7,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_VALUE_7["name"]),
                dict(cti.EXPRESSION_VALUE_8,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_VALUE_8["name"]),
                dict(cti.EXPRESSION_VALUE_9,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_VALUE_9["name"]),
                dict(cti.EXPRESSION_VALUE_10,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_VALUE_10["name"]),
                dict(cti.EXPRESSION_SLICE_1,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_SLICE_1["name"]),
                dict(cti.EXPRESSION_SLICE_2,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_SLICE_2["name"]),
                dict(cti.EXPRESSION_SLICE_3,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_SLICE_3["name"]),
                dict(cti.EXPRESSION_SLICE_4,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_SLICE_4["name"]),
                dict(cti.EXPRESSION_SLICE_5,
                     name="Multi Expression Bytes - "
                     + cti.EXPRESSION_SLICE_5["name"])
            ]
        }
    },
    
    "expression_endpoint_not_implemented": {
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
                "expected_status": [501],
                "schema_file": c.SCHEMA_FILE_EMPTY
            },

            "cases": [

                {
                    "name": "Expression Formats Not Implemented",
                    "description": "request /expressions/formats, "
                        + "expecting 501 status code",
                    "summary_pass": "Expression Formats correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Formats INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Expression Formats Not Implemented' "
                        + "skipped",
                    "url": c.EXPRESSION_API + "formats",
                    "request_params": {}
                },

                {
                    "name": "Expression Ticket by Id Not Implemented",
                    "description": "request /expressions/:id/ticket, "
                        + "expecting 501 status code",
                    "summary_pass": "Expression Ticket by Id correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Ticket by Id INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Expression Ticket by Id Not Implemented' "
                        + "skipped",
                    "url": c.EXPRESSION_API + c.NONEXISTENT_ID + "/ticket",
                    "request_params": {}
                },

                {
                    "name": "Expression Bytes by Id Not Implemented",
                    "description": "request /expressions/:id/bytes, "
                        + "expecting 501 status code",
                    "summary_pass": "Expression Bytes by Id correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Bytes by Id INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Expression Bytes by Id Not Implemented' "
                        + "skipped",
                    "url": c.EXPRESSION_API + c.NONEXISTENT_ID + "/bytes",
                    "request_params": {}
                },

                {
                    "name": "Expression Filters Not Implemented",
                    "description": "request /expressions/filters, "
                        + "expecting 501 status code",
                    "summary_pass": "Expression Filters correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Filters INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Expression Filters Not "
                        + "Implemented' skipped",
                    "url": c.EXPRESSION_API + "filters",
                    "request_params": {}
                },

                {
                    "name": "Expression Ticket Not Implemented",
                    "description": "request /expressions/ticket, "
                        + "expecting 501 status code",
                    "summary_pass": "Expression Ticket correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Ticket INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Expression Ticket Not Implemented' "
                        + "skipped",
                    "url": c.EXPRESSION_API + "ticket",
                    "request_params": {"format": "tsv"}
                },

                {
                    "name": "Expression Bytes Not Implemented",
                    "description": "request /expressions/bytes, "
                        + "expecting 501 status code",
                    "summary_pass": "Expression Bytes correctly "
                        + "non-implemented",
                    "summary_fail": "Expression Bytes INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Expression Bytes Not Implemented' "
                        + "skipped",
                    "url": c.EXPRESSION_API + "bytes",
                    "request_params": {"format": "tsv"}
                }
            ]
        }
    },

    "continuous_formats": {
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
    },

    "continuous_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_filters",
        "description": "Requests the /continuous/filters endpoint.",
        "pass_text": "'Continuous Filters' endpoint correctly "
            + "implemented",
        "fail_text": "'Continuous Filters' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Continuous Filters' test skipped",

        "api": {
            "global_properties": {
                "url": c.CONTINUOUS_API + "filters",
                "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
                "http_method": c.HTTP_GET,
                "request_params": {},
                "server_settings_update_func": uf.update_supported_filters
            },

            "cases": [
                {
                    "name": "Continuous Filters",
                    "description": "request /continuous/filters. checks "
                                   + "content type and status code (200). "
                                   + "validates response body matches search "
                                   + "filter array schema.",
                    "summary_pass": "Continuous filters successfully "
                        + "retrieved",
                    "summary_fail": "Continuous filters NOT retrieved",
                    "summary_skip": "'Continuous Filters' skipped",
                }
            ]
        }
    },
    
    "single_continuous_ticket": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: SINGLE CONTINUOUS TICKET
        # # # # # # # # # # # # # # # # # # # #
        "name": "single_continuous_ticket",
        "description": "Requests the /continuous/:id/ticket endpoint",
        "pass_text": "'Single Continuous Ticket by Id' endpoint correctly "
            + "implemented",
        "fail_text": "'Single Continuous Ticket by Id' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Single Continuous Ticket by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Continuous Ticket",
                    "description": "request /continous/:id/ticket using test "
                        + "continuous id. checks content type and status code "
                        + "(200). validates response body matches Ticket "
                        + "schema",
                    "summary_pass": "Test continuous ticket successfully "
                        + "retrieved",
                    "summary_fail": "Test continuous ticket NOT retrieved",
                    "summary_skip": "'Get Test Continuous Ticket' skipped",
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/ticket",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "server_settings_update_func": uf.update_expected_format
                },

                {
                    "name": "Single Continuous Ticket - Not Found",
                    "description": "request /continuous/:id/ticket using a " 
                        + "continuous id known to not exist. checks "
                        + "content type and status code (4xx). validates "
                        + "response body matches error schema",
                    "summary_pass": "Server sends correct response when "
                        + "requested continuous not found",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when requested continuous not found",
                    "summary_skip": "'Continuous Not Found' skipped",
                    "url": c.CONTINUOUS_API + c.NONEXISTENT_ID + "/ticket",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
                },

                {
                    "name": "Single Continuous Ticket - Start Specified "
                        + "Without Chr",
                    "description": "request /continuous/:id/ticket, "
                        + "specifying start " 
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
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/ticket",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400]
                },

                {
                    "name": "Single Continuous Ticket - End Specified Without "
                        + "Chr",
                    "description": "request /continuous/:id/ticket, "
                        + "specifying end " 
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
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/ticket",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400]
                },

                {
                    "name": "Single Continuous Ticket - Start Greater Than End",
                    "description": "request /continuous/:id/ticket, "
                        + "specifying chr, " 
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
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/ticket",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [501]
                }
            ]
        },

        "content": {
            "global_properties": {
                "tempfile": "single_continuous_ticket_content_test.loom",
                "description": "Assert continuous rows, columns, and cell "
                    + "values match expected",
                "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/ticket",
                "summary_pass": "Continuous matrix content matches expected",
                "summary_fail": "Continuous matrix content DOES NOT match "
                    + "expected",
                "summary_skip": "'Continuous Get Content' test case skipped",
                "download_func": dm.download_from_ticket,
                "request_params_func": \
                    pf.chr_start_end,
            },

            "cases": [
                dict(cti.CONTINUOUS_VALUE_1,
                     name="Single Continuous Ticket - " 
                     + cti.CONTINUOUS_VALUE_1["name"]),
                dict(cti.CONTINUOUS_VALUE_2,
                     name="Single Continuous Ticket - " 
                     + cti.CONTINUOUS_VALUE_2["name"]),
                dict(cti.CONTINUOUS_VALUE_3,
                     name="Single Continuous Ticket - " 
                     + cti.CONTINUOUS_VALUE_3["name"]),
                dict(cti.CONTINUOUS_SLICE_1,
                     name="Single Continuous Ticket - " 
                     + cti.CONTINUOUS_SLICE_1["name"]),
                dict(cti.CONTINUOUS_SLICE_3,
                     name="Single Continuous Ticket - " 
                     + cti.CONTINUOUS_SLICE_3["name"]),
                dict(cti.CONTINUOUS_SLICE_5,
                     name="Single Continuous Ticket - " 
                     + cti.CONTINUOUS_SLICE_5["name"]),
                dict(cti.CONTINUOUS_SLICE_7,
                     name="Single Continuous Ticket - " 
                     + cti.CONTINUOUS_SLICE_7["name"])
            ]
            
        }
    },

    "single_continuous_bytes": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: SINGLE CONTINUOUS BYTES
        # # # # # # # # # # # # # # # # # # # # 
        "name": "single_continuous_bytes",
        "description": "Requests the /continuous/:id/bytes endpoint",
        "pass_text": "'Single Continuous Bytes by Id' endpoint correctly "
            + "implemented",
        "fail_text": "'Single Continuous Bytes by Id' endpoint NOT correctly "
            + "implemented",
        "skip_text": "'Single Continuous Bytes by Id' test skipped",

        "api": {
            "global_properties": {
                "http_method": c.HTTP_GET,
                "request_params": {}
            },

            "cases": [
                {
                    "name": "Get Test Continuous Bytes",
                    "description": "request /continous/:id/bytes using test "
                        + "continuous id. checks content type and status code "
                        + "(200).",
                    "summary_pass": "Test continuous bytes successfully "
                        + "retrieved",
                    "summary_fail": "Test continuous bytes NOT retrieved",
                    "summary_skip": "'Get Test Continuous Bytes' skipped",
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/bytes",
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ],
                    "is_json": False
                },

                {
                    "name": "Single Continuous Bytes - Not Found",
                    "description": "request /continuous/:id/bytes using a " 
                        + "continuous id known to not exist. checks "
                        + "content type and status code (4xx). validates "
                        + "response body matches error schema",
                    "summary_pass": "Server sends correct response when "
                        + "requested continuous not found",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when requested continuous not found",
                    "summary_skip": "'Continuous Not Found' skipped",
                    "url": c.CONTINUOUS_API + c.NONEXISTENT_ID + "/bytes",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400, 404]
                },

                {
                    "name": "Single Continuous Bytes - Start Specified "
                        + "Without Chr",
                    "description": "request /continuous/:id/bytes, "
                        + "specifying start " 
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
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/bytes",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400]
                },

                {
                    "name": "Single Continuous Bytes - End Specified Without "
                        + "Chr",
                    "description": "request /continuous/:id/bytes, "
                        + "specifying end " 
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
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/bytes",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [400]
                },

                {
                    "name": "Single Continuous Bytes - Start Greater Than End",
                    "description": "request /continuous/:id/bytes, "
                        + "specifying chr, " 
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
                    "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/bytes",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "expected_status": [501]
                }
            ]
        },

        "content": {
            "global_properties": {
                "tempfile": "single_continuous_bytes_content_test.loom",
                "description": "Assert continuous rows, columns, and cell "
                    + "values match expected",
                "url": c.CONTINUOUS_API + "V_CONTINUOUS_ID/bytes",
                "summary_pass": "Continuous matrix content matches expected",
                "summary_fail": "Continuous matrix content DOES NOT match "
                    + "expected",
                "summary_skip": "'Continuous Get Content' test case skipped",
                "download_func": dm.download_from_bytes,
                "request_params_func": \
                    pf.chr_start_end,
            },

            "cases": [
                dict(cti.CONTINUOUS_VALUE_3,
                     name="Single Continuous Bytes - " 
                     + cti.CONTINUOUS_VALUE_3["name"]),
                dict(cti.CONTINUOUS_VALUE_4,
                     name="Single Continuous Bytes - " 
                     + cti.CONTINUOUS_VALUE_4["name"]),
                dict(cti.CONTINUOUS_VALUE_5,
                     name="Single Continuous Bytes - " 
                     + cti.CONTINUOUS_VALUE_5["name"]),
                dict(cti.CONTINUOUS_SLICE_2,
                     name="Single Continuous Bytes - " 
                     + cti.CONTINUOUS_SLICE_2["name"]),
                dict(cti.CONTINUOUS_SLICE_4,
                     name="Single Continuous Bytes - " 
                     + cti.CONTINUOUS_SLICE_4["name"]),
                dict(cti.CONTINUOUS_SLICE_6,
                     name="Single Continuous Bytes - " 
                     + cti.CONTINUOUS_SLICE_6["name"]),
                dict(cti.CONTINUOUS_SLICE_8,
                     name="Single Continuous Bytes - " 
                     + cti.CONTINUOUS_SLICE_8["name"])
            ]   
        }
    },
    
    "multi_continuous_ticket": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: MULTI CONTINUOUS TICKET
        # # # # # # # # # # # # # # # # # # # #
        "name": "multi_continuous_ticket",
        "description": "Requests the /continuous/ticket endpoint.",
        "pass_text": "'Continuous Ticket' endpoint correctly implemented",
        "fail_text": "'Continuous Ticket' endpoint NOT correctly implemented",
        "skip_text": "'Continuous Ticket' test skipped",

        "api": {
            "global_properties": {
                "url": c.CONTINUOUS_API + "ticket",
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Continuous Ticket by Format",
                    "description": "requests /continuous/ticket, only "
                       + "specifying the required 'format' parameter. checks "
                       + "content type and status code (200). validates "
                       + "response body matches ticket schema",
                    "summary_pass": "Continuous Ticket can be retrieved",
                    "summary_fail": "Continuous Ticket CANNOT be retrieved",
                    "summary_skip": "'Continuous Ticket by Format' skipped",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Continuous Ticket - All Filters",
                    "description": "request /continuous/ticket using all "
                        + "server-supported continuous filters. checks content "
                        + "type and status code (200). validates response body "
                        + "matches ticket schema.",
                    "summary_pass": "Continuous Ticket retrieved when all "
                        + "filters specified",
                    "summary_fail": "Continuous Ticket CANNOT be retrieved "
                        + "when all filters specified",
                    "summary_skip": "'Continuous Ticket - All Filters' "
                        + "skipped",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "request_params_func": \
                     pf.all_supported_filters_and_format_from_retrieved_settings
                },

                {
                    "name": "Continuous Ticket - Single Filter, 1",
                    "description": "request /continuous/ticket using the "
                        + "first filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200). validates response body "
                        + "matches ticket schema",
                    "summary_pass": "Continuous Ticket retrieved when first "
                        + "filter supplied",
                    "summary_fail": "Continuous Ticket NOT retrieved when "
                        + " first filter supplied",
                    "summary_skip": "'Continuous Ticket - Single Filter, 1' "
                        + "skipped",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "request_params_func": pf.first_supported_filter_and_format
                },

                {
                    "name": "Continuous Ticket - Single Filter, 2",
                    "description": "request /continuous/ticket using the "
                        + "second filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200). validates response body "
                        + "matches ticket schema",
                    "summary_pass": "Continuous Ticket retrieved when second "
                        + "filter supplied",
                    "summary_fail": "Continuous Ticket NOT retrieved when "
                        + "second filter supplied",
                    "summary_skip": "'Continuous Ticket - Single Filter, 2' "
                        + "skipped",
                    "schema_file": c.SCHEMA_FILE_TICKET,
                    "request_params_func": pf.second_supported_filter_and_format
                },

                {
                    "name": "Continuous Ticket - Format Not Specified",
                    "description": "request /continuous/ticket endpoint "
                        + "without specifying the required 'format' parameter. "
                        + "checks content type and status code (4xx). "
                        + "validates response body matches error schema.",
                    "summary_pass": "Server returns error when format not "
                        + "specified",
                    "summary_fail": "Server DOES NOT return error when format "
                        + "not specified",
                    "summary_skip": "'Continuous Ticket - Format Not "
                        + "Specified' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {},
                    "expected_status": [400, 404, 422]
                },

                {
                    "name": "Continuous Ticket - Filetype Matches",
                    "description": "request /continuous/ticket endpoint with "
                        + "'format' parameter specified. checks "
                        + "content type and status code (200). validates "
                        + "ticket fileType matches requested format.",
                    "summary_pass": "Continuous Ticket fileType matches "
                        + "request format",
                    "summary_fail": "Continuous Ticket fileType DOES NOT match "
                        + "request format",
                    "summary_skip": "'Continuous Ticket - Filetypes Match' "
                        + "skipped",
                    "schema_func": sf.schema_require_matching_search_params,
                    "request_params_func": pf.add_format_from_retrieved_settings
                },

                {
                    "name": "Continuous Ticket - Start Specified Without Chr",
                    "description": "request /continuous/ticket, specifying " 
                        + "start parameter without chr. checks content type "
                        + "and status code (400). validates response body "
                        + "matches error schema",
                    "summary_pass": "Server sends correct response when "
                        + "start is specified without chr",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when start is specified without chr",
                    "summary_skip": "'Continuous Ticket - Start Specified "
                        + "Without Chr' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {"start": "5"},
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "expected_status": [400]
                },

                {
                    "name": "Continuous Ticket - End Specified Without Chr",
                    "description": "request /continuous/ticket, specifying " 
                        + "end parameter without chr. checks content type and "
                        + "status code (400). validates response body matches "
                        + "error schema",
                    "summary_pass": "Server sends correct response when "
                        + "end is specified without chr",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when end is specified without chr",
                    "summary_skip": "'Continuous Ticket - End Specified "
                        + "Without Chr' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {"end": "1000"},
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "expected_status": [400]
                },

                {
                    "name": "Continuous Ticket - Start Greater Than End",
                    "description": "request /continuous/ticket, specifying "
                        + "chr, start, and end parameters, but start is " 
                        + "greater than end. checks content type and status "
                        + "code (501). validates response body matches error "
                        + "schema",
                    "summary_pass": "Server sends correct response when "
                        + "start is greater than end",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when start is greater than end",
                    "summary_skip": "'Continuous Ticket - Start Greater Than "
                        + "End' skipped",
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
                "function": cf.continuous_test_case,
                "tempfile": "multi_continuous_ticket_content_test.loom",
                "url": c.CONTINUOUS_API + "ticket",
                "description": "Asserts correct values of continuous matrix, "
                    + "and correct of matrix by parameters (chr, start, end).",
                "summary_pass": "Continuous matrix tracks, positions, and "
                    + "values match expected",
                "summary_fail": "Continuous matrix tracks, positions and "
                    + "values DO NOT match expected",
                "summary_skip": "Continuous content test case skipped",
                "download_func": dm.download_from_ticket,
                "request_params_func": \
                    pf.all_supported_filters_format_chr_start_end,
            },

            "cases": [
                dict(cti.CONTINUOUS_VALUE_1,
                     name="Multi Continuous Ticket - "
                     + cti.CONTINUOUS_VALUE_1["name"]),
                dict(cti.CONTINUOUS_VALUE_3,
                     name="Multi Continuous Ticket - "
                     + cti.CONTINUOUS_VALUE_3["name"]),
                dict(cti.CONTINUOUS_VALUE_5,
                     name="Multi Continuous Ticket - "
                     + cti.CONTINUOUS_VALUE_5["name"]),
                dict(cti.CONTINUOUS_SLICE_1,
                     name="Multi Continuous Ticket - "
                     + cti.CONTINUOUS_SLICE_1["name"]),
                dict(cti.CONTINUOUS_SLICE_3,
                     name="Multi Continuous Ticket - "
                     + cti.CONTINUOUS_SLICE_3["name"]),
                dict(cti.CONTINUOUS_SLICE_5,
                     name="Multi Continuous Ticket - "
                     + cti.CONTINUOUS_SLICE_5["name"]),
                dict(cti.CONTINUOUS_SLICE_7,
                     name="Multi Continuous Ticket - "
                     + cti.CONTINUOUS_SLICE_7["name"])
            ]
        }
    },

    "multi_continuous_bytes": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: MULTI CONTINUOUS BYTES
        # # # # # # # # # # # # # # # # # # # #
        "name": "multi_continuous_bytes",
        "description": "Requests the /continuous/bytes endpoint.",
        "pass_text": "'Continuous Bytes' endpoint correctly implemented",
        "fail_text": "'Continuous Bytes' endpoint NOT correctly implemented",
        "skip_text": "'Continuous Bytes' test skipped",

        "api": {
            "global_properties": {
                "url": c.CONTINUOUS_API + "bytes",
                "http_method": c.HTTP_GET
            },

            "cases": [
                {
                    "name": "Continuous Bytes by Format",
                    "description": "requests /continuous/bytes, only "
                       + "specifying the required 'format' parameter. checks "
                       + "content type and status code (200).",
                    "summary_pass": "Continuous Bytes can be retrieved",
                    "summary_fail": "Continuous Bytes CANNOT be retrieved",
                    "summary_skip": "'Continuous Bytes by Format' skipped",
                    "request_params_func": \
                        pf.add_format_from_retrieved_settings,
                    "is_json": False,
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ]
                },

                {
                    "name": "Continuous Bytes - All Filters",
                    "description": "request /continuous/bytes using all "
                        + "server-supported continuous filters. checks content "
                        + "type and status code (200).",
                    "summary_pass": "Continuous Bytes retrieved when all "
                        + "filters specified",
                    "summary_fail": "Continuous Bytes CANNOT be retrieved "
                        + "when all filters specified",
                    "summary_skip": "'Continuous Bytes - All Filters' "
                        + "skipped",
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "is_json": False,
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ]
                },

                {
                    "name": "Continuous Bytes - Single Filter, 1",
                    "description": "request /continuous/bytes using the "
                        + "first filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200).",
                    "summary_pass": "Continuous Bytes retrieved when first "
                        + "filter supplied",
                    "summary_fail": "Continuous Bytes NOT retrieved when "
                        + " first filter supplied",
                    "summary_skip": "'Continuous Bytes - Single Filter, 1' "
                        + "skipped",
                    "request_params_func": pf.first_supported_filter_and_format,
                    "is_json": False,
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ]
                },

                {
                    "name": "Continuous Bytes - Single Filter, 2",
                    "description": "request /continuous/bytes using the "
                        + "second filter supported by server "
                        + "(in addition to format). checks "
                        + "type and status code (200).",
                    "summary_pass": "Continuous Bytes retrieved when second "
                        + "filter supplied",
                    "summary_fail": "Continuous Bytes NOT retrieved when "
                        + "second filter supplied",
                    "summary_skip": "'Continuous Bytes - Single Filter, 2' "
                        + "skipped",
                    "request_params_func": \
                        pf.second_supported_filter_and_format,
                    "is_json": False,
                    "schema_file": c.SCHEMA_FILE_EMPTY,
                    "use_default_media_types": False,
                    "media_types": [
                        "application/octet-stream",
                        "application/vnd.loom",
                        "text/tab-separated-values"
                    ]
                },

                {
                    "name": "Continuous Bytes - Format Not Specified",
                    "description": "request /continuous/bytes endpoint "
                        + "without specifying the required 'format' parameter. "
                        + "checks content type and status code (4xx). "
                        + "validates response body matches error schema.",
                    "summary_pass": "Server returns error when format not "
                        + "specified",
                    "summary_fail": "Server DOES NOT return error when format "
                        + "not specified",
                    "summary_skip": "'Continuous Bytes - Format Not "
                        + "Specified' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {},
                    "expected_status": [400, 404, 422]
                },

                {
                    "name": "Continuous Bytes - Start Specified Without Chr",
                    "description": "request /continuous/bytes, specifying " 
                        + "start parameter without chr. checks content type "
                        + "and status code (400). validates response body "
                        + "matches error schema",
                    "summary_pass": "Server sends correct response when "
                        + "start is specified without chr",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when start is specified without chr",
                    "summary_skip": "'Continuous Bytes - Start Specified "
                        + "Without Chr' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {"start": "5"},
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "expected_status": [400]
                },

                {
                    "name": "Continuous Bytes - End Specified Without Chr",
                    "description": "request /continuous/bytes, specifying " 
                        + "end parameter without chr. checks content type and "
                        + "status code (400). validates response body matches "
                        + "error schema",
                    "summary_pass": "Server sends correct response when "
                        + "end is specified without chr",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when end is specified without chr",
                    "summary_skip": "'Continuous Bytes - End Specified "
                        + "Without Chr' skipped",
                    "schema_file": c.SCHEMA_FILE_ERROR,
                    "request_params": {"end": "1000"},
                    "request_params_func": \
                    pf.all_supported_filters_and_format_from_retrieved_settings,
                    "expected_status": [400]
                },

                {
                    "name": "Continuous Bytes - Start Greater Than End",
                    "description": "request /continuous/bytes, specifying "
                        + "chr, start, and end parameters, but start is " 
                        + "greater than end. checks content type and status "
                        + "code (501). validates response body matches error "
                        + "schema",
                    "summary_pass": "Server sends correct response when "
                        + "start is greater than end",
                    "summary_fail": "Server DOES NOT send correct response "
                        + "when start is greater than end",
                    "summary_skip": "'Continuous Bytes - Start Greater Than "
                        + "End' skipped",
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
                "function": cf.continuous_test_case,
                "tempfile": "multi_continuous_bytes_content_test.loom",
                "url": c.CONTINUOUS_API + "bytes",
                "description": "Asserts correct values of continuous matrix, "
                    + "and correct of matrix by parameters (chr, start, end).",
                "summary_pass": "Continuous matrix tracks, positions, and "
                    + "values match expected",
                "summary_fail": "Continuous matrix tracks, positions and "
                    + "values DO NOT match expected",
                "summary_skip": "Continuous content test case skipped",
                "download_func": dm.download_from_bytes,
                "request_params_func": \
                    pf.all_supported_filters_format_chr_start_end,
            },

            "cases": [
                dict(cti.CONTINUOUS_VALUE_2,
                     name="Multi Continuous Bytes - "
                     + cti.CONTINUOUS_VALUE_2["name"]),
                dict(cti.CONTINUOUS_VALUE_4,
                     name="Multi Continuous Bytes - "
                     + cti.CONTINUOUS_VALUE_4["name"]),
                dict(cti.CONTINUOUS_VALUE_5,
                     name="Multi Continuous Bytes - "
                     + cti.CONTINUOUS_VALUE_5["name"]),
                dict(cti.CONTINUOUS_SLICE_2,
                     name="Multi Continuous Bytes - "
                     + cti.CONTINUOUS_SLICE_2["name"]),
                dict(cti.CONTINUOUS_SLICE_4,
                     name="Multi Continuous Bytes - "
                     + cti.CONTINUOUS_SLICE_4["name"]),
                dict(cti.CONTINUOUS_SLICE_6,
                     name="Multi Continuous Bytes - "
                     + cti.CONTINUOUS_SLICE_6["name"]),
                dict(cti.CONTINUOUS_SLICE_8,
                     name="Multi Continuous Bytes - "
                     + cti.CONTINUOUS_SLICE_8["name"])
            ]
        }
    },
    
    "continuous_endpoint_not_implemented": {
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
                "expected_status": [501],
                "schema_file": c.SCHEMA_FILE_EMPTY
            },

            "cases": [
                {
                    "name": "Continuous Formats Not Implemented",
                    "description": "request /continuous/formats, "
                        + "expecting 501 status code",
                    "summary_pass": "Continuous Formats correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Formats INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Continuous Formats Not Implemented' "
                        + "skipped",
                    "url": c.CONTINUOUS_API + "formats",
                    "request_params": {}
                },

                {
                    "name": "Continuous Ticket by Id Not Implemented",
                    "description": "request /continuous/:id/ticket, "
                        + "expecting 501 status code",
                    "summary_pass": "Continuous Ticket by Id correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Ticket by Id INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Continuous Ticket by Id Not Implemented' "
                        + "skipped",
                    "url": c.CONTINUOUS_API + c.NONEXISTENT_ID + "/ticket",
                    "request_params": {}
                },

                {
                    "name": "Continuous Bytes by Id Not Implemented",
                    "description": "request /continuous/:id/bytes, "
                        + "expecting 501 status code",
                    "summary_pass": "Continuous Bytes by Id correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Bytes by Id INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Continuous Bytes by Id Not Implemented' "
                        + "skipped",
                    "url": c.CONTINUOUS_API + c.NONEXISTENT_ID + "/bytes",
                    "request_params": {}
                },

                {
                    "name": "Continuous Filters Not Implemented",
                    "description": "request /continuous/filters, "
                        + "expecting 501 status code",
                    "summary_pass": "Continuous Filters correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Filters INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Continuous Filters Not "
                        + "Implemented' skipped",
                    "url": c.CONTINUOUS_API + "filters",
                    "request_params": {}
                },

                {
                    "name": "Continuous Ticket Not Implemented",
                    "description": "request /continuous/ticket, "
                        + "expecting 501 status code",
                    "summary_pass": "Continuous Ticket correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Ticket INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Continuous Ticket Not Implemented' "
                        + "skipped",
                    "url": c.CONTINUOUS_API + "ticket",
                    "request_params": {"format": "tsv"}
                },

                {
                    "name": "Continuous Bytes Not Implemented",
                    "description": "request /continuous/bytes, "
                        + "expecting 501 status code",
                    "summary_pass": "Continuous Bytes correctly "
                        + "non-implemented",
                    "summary_fail": "Continuous Bytes INCORRECTLY "
                        + "non-implemented",
                    "summary_skip": "'Continuous Bytes Not Implemented' "
                        + "skipped",
                    "url": c.CONTINUOUS_API + "bytes",
                    "request_params": {"format": "tsv"}
                }
            ]
        }
    }
}
"""dict: dictionary of dicts, each representing a test scenario"""


TESTS_BY_OBJECT_TYPE = {
    "projects": [
        "project_get",
        "project_filters",
        "project_search"
        
    ],
    "studies": [
        "study_get",
        "study_filters",
        "study_search"
    ],
    "expressions": [
        "expression_formats",
        "expression_filters",
        "single_expression_ticket",
        "single_expression_bytes",
        "multi_expression_ticket",
        "multi_expression_bytes"
    ],
    "continuous": [
        "continuous_formats",
        "continuous_filters",
        "single_continuous_ticket",
        "single_continuous_bytes",
        "multi_continuous_ticket",
        "multi_continuous_bytes"
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
