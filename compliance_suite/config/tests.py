# -*- coding: utf-8 -*-
"""Module compliance_suite.config.tests.py

This module contains all test scenarios as a list of dicts. Each dict contains
specifications for a single test scenario. Each dict serves as input to a
compliance_suite.tests.Test instance constructor.

Attributes:
    TESTS (list): attributes for all test scenarios as a list of dicts
        attributes for each test dictionary:

        name (required): unique name describing the test
        uri (required): URI that request will be sent to (excluding base url)
        schema (required): JSON schema that the response should match
        http_method (required): specify get or post request
        
        pass_text (required): message to display if test is passed
        fail_text (required): message to display if test is failed
        skip_text (required): message to display if test is skipped

        global_params (optional): dictionary of key-value params to be sent
            as part of HTTP request
        params_cases (optional): list of dictionaries, where each list element
            represents a set of key-value params. Can be used to send multiple
            parameter groups and requests for a single test.

Todo:
    * test scenarios for studies, expressions
    * have attribute to capture not OK (!=200) response codes
"""

import compliance_suite.config.constants as c

TESTS = [
    {
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
        "global_params": {},
        "params_cases": [{}]
    }, {
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
        "global_params": {},
        "params_cases": [{}]
    }, {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search",
        "uri": c.PROJECT_API + "search",
        "schema": c.SCHEMA_FILE_PROJECT,
        "http_method": c.HTTP_GET,
        "pass_text": "Projects can be retrieved through the search endpoint",
        "fail_text": "Projects cannot be retrieved through the search endpoint",
        "skip_text": "Project search test skipped",
        "global_params": {},
        "params_cases": [{}]
    }, {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH URL PARAMS
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_url_params",
        "uri": c.PROJECT_API + "search",
        "schema": c.SCHEMA_FILE_PROJECT,
        "http_method": c.HTTP_GET,
        "pass_text": "Projects can be retrieved using URL parameters through"
                     + " the search endpoint",
        "fail_text": "Projects cannot be retrieved using URL parameters through"
                     + " the search endpoint",
        "skip_text": "Project search with URL parameters test skipped",
        "global_params": {"version": "1.0"},
        "params_cases": [{}]
    }, {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH URL PARAMS CASES
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_url_params_cases",
        "uri": c.PROJECT_API + "search",
        "schema": c.SCHEMA_FILE_PROJECT,
        "http_method": c.HTTP_GET,
        "pass_text": "Projects can be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "fail_text": "Projects cannot be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "skip_text": "Project search with multiple URL parameters cases test"
                     + " skipped",
        "global_params": {},
        "params_cases": [{}],
    }, {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_filters",
        "uri": c.PROJECT_API + "search/filters",
        "schema": c.SCHEMA_FILE_PROJECT,
        "http_method": c.HTTP_GET,
        "pass_text": "Project filters can be retrieved through the search "
                     + "endpoint",
        "fail_text": "Project filters cannot be retrieved through the search "
                     + "endpoint",
        "skip_text": "Project filters search test skipped",
        "global_params": {},
        "params_cases": [{}]
    }, {
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
        "global_params": {},
        "params_cases": [{}]
    }, {
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
        "global_params": {},
        "params_cases": [{}]
    }, {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search",
        "uri": c.STUDY_API + "search",
        "schema": c.SCHEMA_FILE_STUDY,
        "http_method": c.HTTP_GET,
        "pass_text": "Studies can be retrieved through the search endpoint",
        "fail_text": "Studies cannot be retrieved through the search endpoint",
        "skip_text": "Study search test skipped",
        "global_params": {},
        "params_cases": [{}]
    }, {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH URL PARAMS
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_url_params",
        "uri": c.STUDY_API + "search",
        "schema": c.SCHEMA_FILE_STUDY,
        "http_method": c.HTTP_GET,
        "pass_text": "Studies can be retrieved using URL parameters through"
                     + " the search endpoint",
        "fail_text": "Studies cannot be retrieved using URL parameters through"
                     + " the search endpoint",
        "skip_text": "Study search with URL parameters test skipped",
        "global_params": {},
        "params_cases": [{}]
    }, {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH URL PARAMS CASES
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_url_params_cases",
        "uri": c.STUDY_API + "search",
        "schema": c.SCHEMA_FILE_STUDY,
        "http_method": c.HTTP_GET,
        "pass_text": "Studies can be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "fail_text": "Studies cannot be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "skip_text": "Study search with multiple URL parameters cases test "
                     + "skipped",
        "global_params": {},
        "params_cases": [{}]
    }, {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_filters",
        "uri": c.STUDY_API + "search/filters",
        "schema": c.SCHEMA_FILE_STUDY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study filters can be retrieved through the search "
                     + "endpoint",
        "fail_text": "Study filters cannot be retrieved through the search "
                     + "endpoint",
        "skip_text": "Study filters search test skipped",
        "global_params": {},
        "params_cases": [{}]
    }, {
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
        "global_params": {},
        "params_cases": [{}]
    }, {
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
        "global_params": {},
        "params_cases": [{}]
    }
]
"""list: list of dicts representing test scenarios"""
