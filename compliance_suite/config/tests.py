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

TESTS_DICT = {
    "project_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT GET
        # # # # # # # # # # # # # # # # # # # # 
        "name": "project_get",
        "description": "Requests the /projects/:id endpoint using project id "
                       + "in config file. Checks content type and status code "
                       + "(200). Validates response body matches project " 
                       + "schema in the specification.",
        "uri": c.PROJECT_API + "V_PROJECT_ID",
        "schema_file": c.SCHEMA_FILE_PROJECT,
        "http_method": c.HTTP_GET,
        "pass_text": "Project endpoint implemented by the server",
        "fail_text": "Project endpoint not implemented by the server",
        "skip_text": "Project endpoint test skipped",
        "apply_params": "no"
    }, "project_get_not_found": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT GET NOT FOUND
        # # # # # # # # # # # # # # # # # # # # 
        "name": "project_get_not_found",
        "description": "Requests the /projects/:id endpoint using a project id "
                       + "that is known to not exist. Checks content type and "
                       + "status code (4xx). Validates response body matches "
                       + "error schema in the specification.",
        "uri": c.PROJECT_API + c.NONEXISTENT_ID,
        "schema_file": c.SCHEMA_FILE_ERROR,
        "http_method": c.HTTP_GET,
        "pass_text": "Project not found endpoint correctly implemented",
        "fail_text": "Project not found endpoint not correctly implemented",
        "skip_text": "Project not found test skipped",
        "apply_params": "no",
        "expected_status": [400, 404]
    }, "project_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search",
        "description": "Requests the /projects/search endpoint without any "
                       + "parameter filters. Checks content type and status "
                       + "code (200). Validates response body matches project "
                       + "array schema in the specification.",
        "uri": c.PROJECT_API + "search",
        "schema_file": c.SCHEMA_FILE_PROJECT_ARRAY_FULL,
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
        "description": "Requests the /projects/search endpoint using all "
                       + "parameter filters in config file. Checks content "
                       + "type and status code (200). Validates response body "
                       + "matches project array schema in the specification.",
        "uri": c.PROJECT_API + "search",
        "schema_file": c.SCHEMA_FILE_PROJECT_ARRAY_FULL,
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
        "description": "Performs multiple requests of the /projects/search "
                       + "endpoint, each time using a different parameter "
                       + "filter in config file. Checks content type and "
                       + "status code (200). Validates response body matches "
                       + "project array schema in the specification.",
        "uri": c.PROJECT_API + "search",
        "schema_file": c.SCHEMA_FILE_PROJECT_ARRAY_FULL,
        "http_method": c.HTTP_GET,
        "pass_text": "Projects can be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "fail_text": "Projects cannot be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "skip_text": "Project search with multiple URL parameters cases test"
                     + " skipped",
        "apply_params": "cases"
    }, "project_search_filters_out": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH FILTERS OUT
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_filters_out",
        "description": "Requests the /projects/search endpoint using "
                       + "parameter filters that do not apply to any project. "
                       + "Checks content type and status code (200). Validates "
                       + "response body is an empty array.",
        "uri": c.PROJECT_API + "search",
        "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Project search endpoint successfully filters out "
                     + "non-matching objects",
        "fail_text": "Project search endpoint does not filter out non-matching "
                     + "objects",
        "skip_text": "Project search filters out test skipped",
        "apply_params": "cases",
        "replace_params": True,
        "param_replacement": c.NONEXISTENT_ID
    }, "project_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: PROJECT SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "project_search_filters",
        "description": "Requests the /projects/search/filters endpoint. " 
                       + "Checks content type and status code (200). Validates "
                       + "response body matches search filter array schema "
                       + "in the specification.",
        "uri": c.PROJECT_API + "search/filters",
        "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
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
        "description": "Requests the /projects/:id endpoint, expecting the "
                       + "endpoint to respond with a 'Not Implemented' status "
                       + "code. Checks content type and status code (501).",
        "uri": c.PROJECT_API + c.NONEXISTENT_ID,
        "schema_file": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Project endpoint correctly not implemented, yields 501 " +
            "status code",
        "fail_text": "Project endpoint incorrectly not implemented, does not " +
            "yield 501 status code",
        "skip_text": "Project endpoint not implemented test skipped",
        "apply_params": "no",
        "expected_status": [501]
    }, "study_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY GET
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_get",
        "description": "Requests the /studies/:id endpoint using study id "
                       + "in config file. Checks content type and status code "
                       + "(200). Validates response body matches study " 
                       + "schema in the specification.",
        "uri": c.STUDY_API + "V_STUDY_ID",
        "schema_file": c.SCHEMA_FILE_STUDY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study endpoint implemented by the server",
        "fail_text": "Study endpoint not implemented by the server",
        "skip_text": "Study endpoint test skipped",
        "apply_params": "no"
    }, "study_get_not_found": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY GET NOT FOUND
        # # # # # # # # # # # # # # # # # # # # 
        "name": "study_get_not_found",
        "description": "Requests the /studies/:id endpoint using a study id "
                       + "that is known to not exist. Checks content type and "
                       + "status code (4xx). Validates response body matches "
                       + "error schema in the specification.",
        "uri": c.STUDY_API + c.NONEXISTENT_ID,
        "schema_file": c.SCHEMA_FILE_ERROR,
        "http_method": c.HTTP_GET,
        "pass_text": "Study not found endpoint correctly implemented",
        "fail_text": "Study not found endpoint not correctly implemented",
        "skip_text": "Study not found test skipped",
        "apply_params": "no",
        "expected_status": [400, 404]
    }, "study_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search",
        "description": "Requests the /studies/search endpoint without any "
                       + "parameter filters. Checks content type and status "
                       + "code (200). Validates response body matches study "
                       + "array schema in the specification.",
        "uri": c.STUDY_API + "search",
        "schema_file": c.SCHEMA_FILE_STUDY_ARRAY_FULL,
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
        "description": "Requests the /studies/search endpoint using all "
                       + "parameter filters in config file. Checks content "
                       + "type and status code (200). Validates response body "
                       + "matches study array schema in the specification.",
        "uri": c.STUDY_API + "search",
        "schema_file": c.SCHEMA_FILE_STUDY_ARRAY_FULL,
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
        "description": "Performs multiple requests of the /studies/search "
                       + "endpoint, each time using a different parameter "
                       + "filter in config file. Checks content type and "
                       + "status code (200). Validates response body matches "
                       + "study array schema in the specification.",
        "uri": c.STUDY_API + "search",
        "schema_file": c.SCHEMA_FILE_STUDY_ARRAY_FULL,
        "http_method": c.HTTP_GET,
        "pass_text": "Studies can be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "fail_text": "Studies cannot be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "skip_text": "Study search with multiple URL parameters cases test "
                     + "skipped",
        "apply_params": "cases"
    }, "study_search_filters_out": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH FILTERS OUT
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_filters_out",
        "description": "Requests the /studies/search endpoint using "
                       + "parameter filters that do not apply to any study. "
                       + "Checks content type and status code (200). Validates "
                       + "response body is an empty array.",
        "uri": c.STUDY_API + "search",
        "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study search endpoint successfully filters out "
                     + "non-matching objects",
        "fail_text": "Study search endpoint does not filter out non-matching "
                     + "objects",
        "skip_text": "Study search filters out test skipped",
        "apply_params": "cases",
        "replace_params": True,
        "param_replacement": c.NONEXISTENT_ID
    }, "study_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: STUDY SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "study_search_filters",
        "description": "Requests the /studies/search/filters endpoint. " 
                       + "Checks content type and status code (200). Validates "
                       + "response body matches search filter array schema "
                       + "in the specification.",
        "uri": c.STUDY_API + "search/filters",
        "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
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
        "description": "Requests the /studies/:id endpoint, expecting the "
                       + "endpoint to respond with a 'Not Implemented' status "
                       + "code. Checks content type and status code (501).",
        "uri": c.STUDY_API + c.NONEXISTENT_ID,
        "schema_file": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Study endpoint correctly not implemented, yields 501 " +
            "status code",
        "fail_text": "Study endpoint incorrectly not implemented, does not " +
            "yield 501 status code",
        "skip_text": "Study endpoint not implemented test skipped",
        "apply_params": "no",
        "expected_status": [501]
    }, "expression_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION GET
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_get",
        "description": "Requests the /expressions/:id endpoint using "
                       + "expression id in config file. Checks content type "
                       + "and status code (200). Validates response body "
                       + "matches project schema in the specification.",
        "uri": c.EXPRESSION_API + "V_EXPRESSION_ID",
        "schema_file": c.SCHEMA_FILE_EXPRESSION,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression endpoint implemented by the server",
        "fail_text": "Expression endpoint not implemented by the server",
        "skip_text": "Expression endpoint test skipped",
        "apply_params": "no"
    }, "expression_get_not_found": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION GET NOT FOUND
        # # # # # # # # # # # # # # # # # # # # 
        "name": "expression_get_not_found",
        "description": "Requests the /expressions/:id endpoint using an "
                       + "expression id that is known to not exist. Checks "
                       + "content type and status code (4xx). Validates "
                       + "response body matches error schema in the "
                       + "specification",
        "uri": c.EXPRESSION_API + c.NONEXISTENT_ID,
        "schema_file": c.SCHEMA_FILE_ERROR,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression not found endpoint correctly implemented",
        "fail_text": "Expression not found endpoint not correctly implemented",
        "skip_text": "Expression not found test skipped",
        "apply_params": "no",
        "expected_status": [400, 404]
    }, "expression_formats": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION FORMATS
        # # # # # # # # # # # # # # # # # # # # 
        "name": "expression_formats",
        "description": "Requests the /expressions/formats endpoint. Checks "
                       + "content type and status code (200). Validates "
                       + "response body is an array of strings.",
        "uri": c.EXPRESSION_API + "formats",
        "schema_file": c.SCHEMA_FILE_STRING_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression formats endpoint implemented",
        "fail_text": "Expression formats endpoint not implemented",
        "skip_text": "Expression formats test skipped",
        "apply_params": "no",
    }, "expression_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search",
        "description": "Requests the /expressions/search endpoint, only "
                       + "specifying the required 'format' parameter. Checks "
                       + "content type and status code (200). Validates "
                       + "response body matches expression array schema in the "
                       + "specification.",
        "uri": c.EXPRESSION_API + "search",
        "schema_file": c.SCHEMA_FILE_EXPRESSION_ARRAY_FULL,
        "http_method": c.HTTP_GET,
        "pass_text": "Expressions can be retrieved through search endpoint",
        "fail_text": "Expressions cannot be retrieved through search endpoint",
        "skip_text": "Expression search test skipped",
        "apply_params": "some",
        "specified_params": ["format"]
    }, "expression_search_url_params_all": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH URL PARAMS ALL
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_url_params_all",
        "description": "Requests the /expressions/search endpoint using all "
                       + "parameter filters in config file. Checks content "
                       + "type and status code (200). Validates response body "
                       + "matches expressions array schema in the "
                       + "specification.",
        "uri": c.EXPRESSION_API + "search",
        "schema_file": c.SCHEMA_FILE_EXPRESSION_ARRAY_FULL,
        "http_method": c.HTTP_GET,
        "pass_text": "Expressions can be retrieved using URL parameters through"
                     + " the search endpoint",
        "fail_text": "Expressions cannot be retrieved using URL parameters "
                     + " through the search endpoint",
        "skip_text": "Expression search with URL parameters test skipped",
        "apply_params": "all"
    }, "expression_search_url_params_cases": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH URL PARAMS CASES
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_url_params_cases",
        "description": "Performs multiple requests of the /expressions/search "
                       + "endpoint, each time using a different parameter "
                       + "filter in config file. Checks content type and "
                       + "status code (200). Validates response body matches "
                       + "expression array schema in the specification.",
        "uri": c.EXPRESSION_API + "search",
        "schema_file": c.SCHEMA_FILE_EXPRESSION_ARRAY_FULL,
        "http_method": c.HTTP_GET,
        "pass_text": "Expressions can be retrieved using URL parameters through"
                     + " the search endpoint for all cases",
        "fail_text": "Expressions cannot be retrieved using URL parameters "
                     + " through the search endpoint for all cases",
        "skip_text": "Expressions search with multiple URL parameters cases "
                     + " test skipped",
        "apply_params": "cases",
        "specified_params": ["format"]
    }, "expression_search_filters_out": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH FILTERS OUT
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_filters_out",
        "description": "Requests the /expressions/search endpoint using "
                       + "parameter filters that do not apply to any "
                       + "expression. Checks content type and status code "
                       + "(200). Validates response body is an empty array.",
        "uri": c.EXPRESSION_API + "search",
        "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression search endpoint successfully filters out "
                     + "non-matching objects",
        "fail_text": "Expression search endpoint does not filter out "
                     + "non-matching objects",
        "skip_text": "Expression search filters out test skipped",
        "apply_params": "cases",
        "specified_params": ["format"],
        "replace_params": True,
        "param_replacement": c.NONEXISTENT_ID
    }, "expression_search_format_not_specified": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH FORMAT NOT SPECIFIED
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_format_not_specified",
        "description": "Requests the /expressions/search endpoint without "
                       + "specifying the required 'format' parameter. Checks "
                       + "content type and status code (4xx). Validates "
                       + "response body is an error message JSON.",
        "uri": c.EXPRESSION_API + "search",
        "schema_file": c.SCHEMA_FILE_ERROR,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression search endpoint appropriately raises error "
                     + "when format not specified",
        "fail_text": "Expression search endpoint does not raise error when "
                     + "format not specified",
        "skip_text": "Expression search format not specified test skipped",
        "apply_params": "no",
        "expected_status": [400, 404, 422]
    }, "expression_search_filetypes_match": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH FILETYPES MATCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_filetypes_match",
        "description": "Requests the /expressions/search endpoint with "
                       + "'format' parameter specified. Checks "
                       + "content type and status code (200). Validates "
                       + "expression objects in response body contain a "
                       + "fileType that matches the requested format.",
        "uri": c.EXPRESSION_API + "search",
        "schema_func": sf.schema_expression_search_filetypes_match,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression search returns expression objects with "
                     + "fileType matching specified format",
        "fail_text": "Expression search does not return expression objects "
                     + "with fileType matching specified format",
        "skip_text": "Expression search filetypes match test skipped",
        "apply_params": "some",
        "specified_params": ["format"],
    }, "expression_search_no_filetype_mismatches": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH NO FILETYPE MISMATCHES
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_no_filetype_mismatches",
        "description": "Requests the /expressions/search endpoint with "
                       + "'format' parameter that does not match the format "
                       + "specified in config file. Checks content type and "
                       + "status code (200). Validates expression objects in "
                       + "response body have a fileType matching the requested "
                       + "format.",
        "uri": c.EXPRESSION_API + "search",
        "schema_func": sf.schema_expression_search_no_filetype_mismatches,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression search returns expression objects with "
                     + "fileType matching specified format when requested "
                     + "format is modified",
        "fail_text": "Expression search does not return expression objects "
                     + "with fileType matching specified format when "
                     + "requested formate is modified",
        "skip_text": "Expression search no filetype mismatches test skipped",
        "apply_params": "some",
        "replace_params": True,
        "param_func": pf.switch_format_param,
        "specified_params": ["format"],
    }, "expression_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "expression_search_filters",
        "description": "Requests the /expressions/search/filters endpoint. " 
                       + "Checks content type and status code (200). Validates "
                       + "response body matches search filter array schema "
                       + "in the specification.",
        "uri": c.EXPRESSION_API + "search/filters",
        "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression filters can be retrieved through the search "
                     + "endpoint",
        "fail_text": "Expression filters cannot be retrieved through the "
                     + "search endpoint",
        "skip_text": "Expression filters search test skipped",
        "apply_params": "no"
    }, "expression_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: EXPRESSION ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "expression_endpoint_not_implemented",
        "description": "Requests the /expressions/:id endpoint, expecting the "
                       + "endpoint to respond with a 'Not Implemented' status "
                       + "code. Checks content type and status code (501).",
        "uri": c.EXPRESSION_API + c.NONEXISTENT_ID,
        "schema_file": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Expression endpoint correctly not implemented, " +
            "yields 501 status code",
        "fail_text": "Expression endpoint incorrectly not implemented, does " +
            "not yield 501 status code",
        "skip_text": "Expression endpoint not implemented test skipped",
        "apply_params": "no",
        "expected_status": [501]
    }, "continuous_get": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS GET
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_get",
        "description": "Requests the /continuous/:id endpoint using continuous "
                       + "id in config file. Checks content type and status "
                       + "code (200).",
        "uri": c.CONTINUOUS_API + "V_CONTINUOUS_ID",
        "schema_file": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous endpoint implemented by the server",
        "fail_text": "Continuous endpoint not implemented by the server",
        "skip_text": "Continuous endpoint test skipped",
        "apply_params": "no",
        "use_default_media_types": False,
        "media_types": ["application/vnd.loom", "text/tab-separated-values"],
        "is_json": False
    }, "continuous_get_not_found": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS GET NOT FOUND
        # # # # # # # # # # # # # # # # # # # # 
        "name": "continuous_get_not_found",
        "description": "Requests the /continuous/:id endpoint using a " 
                       + "continuous id that is known to not exist. Checks "
                       + "content type and status code (4xx). Validates "
                       + "response body matches error schema in the "
                       + "specification",
        "uri": c.CONTINUOUS_API + c.NONEXISTENT_ID,
        "schema_file": c.SCHEMA_FILE_ERROR,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous not found endpoint correctly implemented",
        "fail_text": "Continuous not found endpoint not correctly implemented",
        "skip_text": "Continuous not found test skipped",
        "apply_params": "no",
        "expected_status": [400, 404]
    }, "continuous_formats": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS FORMATS
        # # # # # # # # # # # # # # # # # # # # 
        "name": "continuous_formats",
        "description": "Requests the /continuous/formats endpoint. Checks "
                       + "content type and status code (200). Validates "
                       + "response body is an array of strings.",
        "uri": c.CONTINUOUS_API + "formats",
        "schema_file": c.SCHEMA_FILE_STRING_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous formats endpoint implemented",
        "fail_text": "Continuous formats endpoint not implemented",
        "skip_text": "Continuous formats test skipped",
        "apply_params": "no",
    }, "continuous_search": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search",
        "description": "Requests the /continuous/search endpoint, only "
                       + "specifying the required 'format' parameter. Checks "
                       + "content type and status code (200). Validates "
                       + "response body matches continuous array schema in the "
                       + "specification.",
        "uri": c.CONTINUOUS_API + "search",
        "schema_file": c.SCHEMA_FILE_CONTINUOUS_ARRAY_FULL,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous objects can be retrieved through search "
            + "endpoint",
        "fail_text": "Continuous objects cannot be retrieved through search "
            + "endpoint",
        "skip_text": "Continuous search test skipped",
        "apply_params": "some",
        "specified_params": ["format"]
    }, "continuous_search_url_params_all": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH URL PARAMS ALL
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_url_params_all",
        "description": "Requests the /continuous/search endpoint using all "
                       + "parameter filters in config file. Checks content "
                       + "type and status code (200). Validates response body "
                       + "matches continuous object array schema in the "
                       + "specification.",
        "uri": c.CONTINUOUS_API + "search",
        "schema_file": c.SCHEMA_FILE_CONTINUOUS_ARRAY_FULL,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous objects can be retrieved using URL parameters "
                     + "through the search endpoint",
        "fail_text": "Continuous objects cannot be retrieved using URL " 
                     + "parameters through the search endpoint",
        "skip_text": "Continuous search with URL parameters test skipped",
        "apply_params": "all"
    }, "continuous_search_url_params_cases": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH URL PARAMS CASES
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_url_params_cases",
        "description": "Performs multiple requests of the /continuous/search "
                       + "endpoint, each time using a different parameter "
                       + "filter in config file. Checks content type and "
                       + "status code (200). Validates response body matches "
                       + "continuous array schema in the specification.",
        "uri": c.CONTINUOUS_API + "search",
        "schema_file": c.SCHEMA_FILE_CONTINUOUS_ARRAY_FULL,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous objects can be retrieved using URL parameters "
                     + "through the search endpoint for all cases",
        "fail_text": "Continuous objects cannot be retrieved using URL "
                     + "parameters through the search endpoint for all cases",
        "skip_text": "Continuous search with multiple URL parameters cases "
                     + " test skipped",
        "apply_params": "cases",
        "specified_params": ["format"]
    }, "continuous_search_filters_out": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH FILTERS OUT
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_filters_out",
        "description": "Requests the /continuous/search endpoint using "
                       + "parameter filters that do not apply to any "
                       + "continuous object. Checks content type and status "
                       + "code (200). Validates response body is an empty "
                       + "array.",
        "uri": c.CONTINUOUS_API + "search",
        "schema_file": c.SCHEMA_FILE_EMPTY_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous search endpoint successfully filters out "
                     + "non-matching objects",
        "fail_text": "Continuous search endpoint does not filter out "
                     + "non-matching objects",
        "skip_text": "Continuous search filters out test skipped",
        "apply_params": "cases",
        "specified_params": ["format"],
        "replace_params": True,
        "param_replacement": c.NONEXISTENT_ID
    }, "continuous_search_format_not_specified": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH FORMAT NOT SPECIFIED
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_format_not_specified",
        "description": "Requests the /continuous/search endpoint without "
                       + "specifying the required 'format' parameter. Checks "
                       + "content type and status code (4xx). Validates "
                       + "response body is an error message JSON.",
        "uri": c.CONTINUOUS_API + "search",
        "schema_file": c.SCHEMA_FILE_ERROR,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous search endpoint appropriately raises error "
                     + "when format not specified",
        "fail_text": "Continuous search endpoint does not raise error when "
                     + "format not specified",
        "skip_text": "Continuous search format not specified test skipped",
        "apply_params": "no",
        "expected_status": [400, 404, 422]
    }, "continuous_search_formats_match": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH FORMATS MATCH
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_formats_match",
        "description": "Requests the /continuous/search endpoint with "
                       + "'format' parameter specified. Checks "
                       + "content type and status code (200). Validates "
                       + "continuous objects in response body contain a "
                       + "format that matches the format in the request.",
        "uri": c.CONTINUOUS_API + "search",
        "schema_func": sf.schema_continuous_search_formats_match,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous search returns objects with "
                     + "format matching request",
        "fail_text": "Continuous search does not return objects "
                     + "with format matching request",
        "skip_text": "Continuous search formats match test skipped",
        "apply_params": "some",
        "specified_params": ["format"],
    }, "continuous_search_no_format_mismatches": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH NO FORMAT MISMATCHES
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_no_format_mismatches",
        "description": "Requests the /continuous/search endpoint with "
                       + "'format' parameter that does not match the format "
                       + "specified in config file. Checks content type and "
                       + "status code (200). Validates continuous objects in "
                       + "response body have a fileType matching the request.",
        "uri": c.CONTINUOUS_API + "search",
        "schema_func": sf.schema_continuous_search_no_format_mismatches,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous search returns objects with fileType matching "
                     + "requested format when modified",
        "fail_text": "Continuous search does not return objects with fileType"
                     + "matching requested format when modified",
        "skip_text": "Continuous search no format mismatches test skipped",
        "apply_params": "some",
        "replace_params": True,
        "param_replacement": c.NONEXISTENT_ID,
        "specified_params": ["format"],
    }, "continuous_search_filters": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS SEARCH FILTERS
        # # # # # # # # # # # # # # # # # # # #
        "name": "continuous_search_filters",
        "description": "Requests the /continuous/search/filters endpoint. " 
                       + "Checks content type and status code (200). Validates "
                       + "response body matches search filter array schema "
                       + "in the specification.",
        "uri": c.CONTINUOUS_API + "search/filters",
        "schema_file": c.SCHEMA_FILE_SEARCH_FILTER_ARRAY,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous filters can be retrieved through the search "
                     + "endpoint",
        "fail_text": "Continuous filters cannot be retrieved through the "
                     + "search endpoint",
        "skip_text": "Continous filters search test skipped",
        "apply_params": "no"
    }, "continuous_endpoint_not_implemented": {
        # # # # # # # # # # # # # # # # # # # #
        # TEST: CONTINUOUS ENDPOINT NOT IMPLEMENTED
        # # # # # # # # # # # # # # # # # # # # 
        "name": "continuous_endpoint_not_implemented",
        "description": "Requests the /continuous/:id endpoint, expecting the "
                       + "endpoint to respond with a 'Not Implemented' status "
                       + "code. Checks content type and status code (501).",
        "uri": c.CONTINUOUS_API + c.NONEXISTENT_ID,
        "schema_file": c.SCHEMA_FILE_EMPTY,
        "http_method": c.HTTP_GET,
        "pass_text": "Continuous endpoint correctly not implemented, " +
            "yields 501 status code",
        "fail_text": "Continuous endpoint incorrectly not implemented, does " +
            "not yield 501 status code",
        "skip_text": "Continuous endpoint not implemented test skipped",
        "apply_params": "no",
        "expected_status": [501]
    }
}
"""dict: dictionary of dicts, each representing a test scenario"""

TESTS_BY_OBJECT_TYPE = {
    "projects": [
        "project_get",
        "project_get_not_found",
        "project_search",
        "project_search_url_params_all",
        "project_search_url_params_cases",
        "project_search_filters_out",
        "project_search_filters"
    ],
    "studies": [
        "study_get",
        "study_get_not_found",
        "study_search",
        "study_search_url_params_all",
        "study_search_url_params_cases",
        "study_search_filters_out",
        "study_search_filters"
    ],
    "expressions": [
        "expression_get",
        "expression_get_not_found",
        "expression_formats",
        "expression_search",
        "expression_search_url_params_all",
        "expression_search_url_params_cases",
        "expression_search_filters_out",
        "expression_search_format_not_specified",
        "expression_search_filetypes_match",
        "expression_search_no_filetype_mismatches",
        "expression_search_filters"
    ],
    "continuous": [
        "continuous_get",
        "continuous_get_not_found",
        "continuous_formats",
        "continuous_search",
        "continuous_search_url_params_all",
        "continuous_search_url_params_cases",
        "continuous_search_filters_out",
        "continuous_search_format_not_specified",
        "continuous_search_formats_match",
        "continuous_search_no_format_mismatches",
        "continuous_search_filters"
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