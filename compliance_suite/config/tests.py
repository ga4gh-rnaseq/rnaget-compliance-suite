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
        schema (required): JSON schema that the response should match
        http_method (required): specify get or post request
        pass_text (required): message to display if test is passed
        fail_text (required): message to display if test is failed
        skip_text (required): message to display if test is skipped
        apply_params (required): "all" if all param filters applied at once,
            "cases" if param filters tested one at a time, "no" if params not
            applied at all
        expected_status (optional): int indicating expected response code. If
            nothing specified, test expects OK status code (200)
    
    TESTS_BY_OBJECT_TYPE (dict): lists the name of tests grouped by the object
        type they pertain to (project, study, expression)
    
    NOT_IMPLEMENTED_TESTS_BY_OBJECT_TYPE (dict): lists the name of tests
        associated with non-implemented endpoints, grouped by the object type
        they pertain to. Non-implemented endpoints must still be correctly
        configured, ie must yield 501 response.

Todo:
    * test scenarios for studies, expressions
    * have attribute to capture not OK (!=200) response codes
"""

import compliance_suite.config.constants as c

TESTS_DICT = {
    "project_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT GET
        # # # # # # # # # # # # # # # # # # # # 
        "name": "project_get",
        "uri": c.PROJECT_API + "V_PROJECT_ID",
        "schema": c.SCHEMA_FILE_PROJECT,
        "http_method": c.HTTP_GET,
        "pass_text": "Project endpoint implemented by the server",
        "fail_text": "Project endpoint not implemented by the server",
        "skip_text": "Project endpoint test skipped",
        "apply_params": "no"
    }, "project_get_default": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT GET DEFAULT
        # # # # # # # # # # # # # # # # # # # # 
        "name": "project_get_default",
        "uri": c.PROJECT_API + "V_PROJECT_ID",
        "schema": c.SCHEMA_FILE_PROJECT,
        "http_method": c.HTTP_GET,
        "pass_text": "Project endpoint implemented with default encoding",
        "fail_text": "Project endpoint not implemented with default encoding",
        "skip_text": "Project endpoint default encoding test skipped",
        "apply_params": "no"
    }, "project_get_not_found": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT GET NOT FOUND
        # # # # # # # # # # # # # # # # # # # # 
        "name": "project_get_not_found",
        "uri": c.PROJECT_API + c.NONEXISTENT_ID,
        "schema": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Project not found endpoint correctly implemented",
        "fail_text": "Project not found endpoint not correctly implemented",
        "skip_text": "Project not found test skipped",
        "apply_params": "no",
        "expected_status": 404
    }, "project_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search",
        "uri": c.PROJECT_API + "search",
        "schema": c.SCHEMA_FILE_PROJECT_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Projects can be retrieved through the search endpoint",
        "fail_text": "Projects cannot be retrieved through the search endpoint",
        "skip_text": "Project search test skipped",
        "apply_params": "no"
    }, "project_search_url_params_all": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH URL PARAMS ALL
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_url_params_all",
        "uri": c.PROJECT_API + "search",
        "schema": c.SCHEMA_FILE_PROJECT_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Projects can be retrieved using URL parameters through"
                     + " the search endpoint",
        "fail_text": "Projects cannot be retrieved using URL parameters through"
                     + " the search endpoint",
        "skip_text": "Project search with URL parameters test skipped",
        "apply_params": "all"
    }, "project_search_url_params_cases": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH URL PARAMS CASES
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_url_params_cases",
        "uri": c.PROJECT_API + "search",
        "schema": c.SCHEMA_FILE_PROJECT_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Projects can be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "fail_text": "Projects cannot be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "skip_text": "Project search with multiple URL parameters cases test"
                     + " skipped",
        "apply_params": "cases"
    }, "project_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_filters",
        "uri": c.PROJECT_API + "search/filters",
        "schema": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Project filters can be retrieved through the search "
                     + "endpoint",
        "fail_text": "Project filters cannot be retrieved through the search "
                     + "endpoint",
        "skip_text": "Project filters search test skipped",
        "apply_params": "no"
    }, "project_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "project_endpoint_not_implemented",
        "uri": c.PROJECT_API + c.NONEXISTENT_ID,
        "schema": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Project endpoint correctly not implemented, yields 501 " +
            "status code",
        "fail_text": "Project endpoint incorrectly not implemented, does not " +
            "yield 501 status code",
        "skip_text": "Project endpoint not implemented test skipped",
        "apply_params": "no",
        "expected_status": 501
    }, "study_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY GET
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_get",
        "uri": c.STUDY_API + "V_STUDY_ID",
        "schema": c.SCHEMA_FILE_STUDY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study endpoint implemented by the server",
        "fail_text": "Study endpoint not implemented by the server",
        "skip_text": "Study endpoint test skipped",
        "apply_params": "no"
    }, "study_get_default": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY GET DEFAULT
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_get_default",
        "uri": c.STUDY_API + "V_STUDY_ID",
        "schema": c.SCHEMA_FILE_STUDY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study endpoint implemented with default encoding",
        "fail_text": "Study endpoint not implemented with default encoding",
        "skip_text": "Study endpoint default encoding test skipped",
        "apply_params": "no"
    }, "study_get_not_found": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY GET NOT FOUND
        # # # # # # # # # # # # # # # # # # # # 
        "name": "study_get_not_found",
        "uri": c.STUDY_API + c.NONEXISTENT_ID,
        "schema": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study not found endpoint correctly implemented",
        "fail_text": "Study not found endpoint not correctly implemented",
        "skip_text": "Study not found test skipped",
        "apply_params": "no",
        "expected_status": 404
    }, "study_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search",
        "uri": c.STUDY_API + "search",
        "schema": c.SCHEMA_FILE_STUDY_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Studies can be retrieved through the search endpoint",
        "fail_text": "Studies cannot be retrieved through the search endpoint",
        "skip_text": "Study search test skipped",
        "apply_params": "no"
    }, "study_search_url_params_all": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH URL PARAMS ALL
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_url_params_all",
        "uri": c.STUDY_API + "search",
        "schema": c.SCHEMA_FILE_STUDY_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Studies can be retrieved using URL parameters through"
                     + " the search endpoint",
        "fail_text": "Studies cannot be retrieved using URL parameters through"
                     + " the search endpoint",
        "skip_text": "Study search with URL parameters test skipped",
        "apply_params": "all"
    }, "study_search_url_params_cases": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH URL PARAMS CASES
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_url_params_cases",
        "uri": c.STUDY_API + "search",
        "schema": c.SCHEMA_FILE_STUDY_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Studies can be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "fail_text": "Studies cannot be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "skip_text": "Study search with multiple URL parameters cases test "
                     + "skipped",
        "apply_params": "cases"
    }, "study_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_filters",
        "uri": c.STUDY_API + "search/filters",
        "schema": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study filters can be retrieved through the search "
                     + "endpoint",
        "fail_text": "Study filters cannot be retrieved through the search "
                     + "endpoint",
        "skip_text": "Study filters search test skipped",
        "apply_params": "no"
    }, "study_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "study_endpoint_not_implemented",
        "uri": c.STUDY_API + c.NONEXISTENT_ID,
        "schema": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study endpoint correctly not implemented, yields 501 " +
            "status code",
        "fail_text": "Study endpoint incorrectly not implemented, does not " +
            "yield 501 status code",
        "skip_text": "Study endpoint not implemented test skipped",
        "apply_params": "no",
        "expected_status": 501
    }, "expression_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION GET
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_get",
        "uri": c.EXPRESSION_API + "V_EXPRESSION_ID",
        "schema": c.SCHEMA_FILE_EXPRESSION,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression endpoint implemented by the server",
        "fail_text": "Expression endpoint not implemented by the server",
        "skip_text": "Expression endpoint test skipped",
        "apply_params": "no"
    }, "expression_get_default": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION GET DEFAULT
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_get_default",
        "uri": c.EXPRESSION_API + "V_EXPRESSION_ID",
        "schema": c.SCHEMA_FILE_EXPRESSION,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression endpoint implemented with default encoding",
        "fail_text": "Expression endpoint not implemented with default "
                     + "encoding",
        "skip_text": "Expression endpoint default encoding test skipped",
        "apply_params": "no"
    }, "expression_get_not_found": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION GET NOT FOUND
        # # # # # # # # # # # # # # # # # # # # 
        "name": "expression_get_not_found",
        "uri": c.EXPRESSION_API + c.NONEXISTENT_ID,
        "schema": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression not found endpoint correctly implemented",
        "fail_text": "Expression not found endpoint not correctly implemented",
        "skip_text": "Expression not found test skipped",
        "apply_params": "no",
        "expected_status": 404
    }, "expression_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "expression_endpoint_not_implemented",
        "uri": c.EXPRESSION_API + c.NONEXISTENT_ID,
        "schema": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression endpoint correctly not implemented, " +
            "yields 501 status code",
        "fail_text": "Expression endpoint incorrectly not implemented, does " +
            "not yield 501 status code",
        "skip_text": "Expression endpoint not implemented test skipped",
        "apply_params": "no",
        "expected_status": 501
    }, "continuous_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS GET
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_get",
        "uri": c.CONTINUOUS_API + "V_CONTINUOUS_ID",
        "schema": c.SCHEMA_FILE_CONTINUOUS,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuos endpoint implemented by the server",
        "fail_text": "Continuos endpoint not implemented by the server",
        "skip_text": "Continuos endpoint test skipped",
        "apply_params": "no"
    }, "continuous_get_default": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS GET DEFAULT
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_get_default",
        "uri": c.CONTINUOUS_API + "V_CONTINUOUS_ID",
        "schema": c.SCHEMA_FILE_CONTINUOUS,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous endpoint implemented with default encoding",
        "fail_text": "Continuous endpoint not implemented with default "
                     + "encoding",
        "skip_text": "Continuous endpoint default encoding test skipped",
        "apply_params": "no"
    }, "continuous_get_not_found": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS GET NOT FOUND
        # # # # # # # # # # # # # # # # # # # # 
        "name": "continuous_get_not_found",
        "uri": c.CONTINUOUS_API + c.NONEXISTENT_ID,
        "schema": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous not found endpoint correctly implemented",
        "fail_text": "Continuous not found endpoint not correctly implemented",
        "skip_text": "Continuous not found test skipped",
        "apply_params": "no",
        "expected_status": 404
    }, "continuous_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "continuous_endpoint_not_implemented",
        "uri": c.CONTINUOUS_API + c.NONEXISTENT_ID,
        "schema": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous endpoint correctly not implemented, " +
            "yields 501 status code",
        "fail_text": "Continuous endpoint incorrectly not implemented, does " +
            "not yield 501 status code",
        "skip_text": "Continuous endpoint not implemented test skipped",
        "apply_params": "no",
        "expected_status": 501
    }
}
"""dict: dictionary of dicts, each representing a test scenario"""

TESTS_BY_OBJECT_TYPE = {
    "projects": [
        "project_get",
        "project_get_default",
        "project_get_not_found",
        "project_search",
        "project_search_url_params_all",
        "project_search_url_params_cases",
        "project_search_filters"
    ],
    "studies": [
        "study_get",
        "study_get_default",
        "study_get_not_found",
        "study_search",
        "study_search_url_params_all",
        "study_search_url_params_cases",
        "study_search_filters"
    ],
    "expressions": [
        "expression_get",
        "expression_get_default",
        "expression_get_not_found"
    ],
    "continuous": [
        "continuous_get",
        "continuous_get_default",
        "continuous_get_not_found"
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