# -*- coding: utf-8 -*-
"""Module compliance_suite.single_test_executor.py

This module contains class definition for generalized model of testing an api
route. The SingleTestExecutor executes a request, checks status code of the
response, validates the schema of the returned JSON object against the
corresponding schema, and sets the test result to 1 (success) or -1 (fail)

Todo:
    * handle query parameters
    * handle tests for not OK (!=200) response codes
"""

import requests

from compliance_suite.schema_validator import SchemaValidator
from compliance_suite.config.constants import *

class SingleTestExecutor(object):
    """Executes API request, validates response and sets result to pass/fail

    The SingleTestExecutor is a generalized model for executing tests against
    the API. It executes a request, checks for response code, and validates
    the returned object against a schema.

    Attributes:
        uri (str): uri to be requested
        schema_file (str): JSON schema file to validate response against
        http_method (int): GET or POST request
        params (dict): parameters/filters to submit with query
        test (Test): reference to Test object
        runner (TestRunner): reference to TestRunner object
    """

    def __init__(self, uri, schema_file, http_method, params, test, runner):
        """instantiates a SingleTestExecutor object
        
        Args:
            uri (str): uri to be requested
            schema_file (str): JSON schema file to validate response against
            http_method (int): GET or POST request
            params (dict): parameters/filters to submit with query
            test (Test): reference to Test object
            runner (TestRunner): reference to TestRunner object
        """

        self.uri = uri
        self.schema_file = schema_file
        self.http_method = http_method
        self.params = params
        self.test = test
        self.runner = runner
        self.headers = ACCEPT_HEADER
    
    def execute_test(self):
        """Test API URI, validate response and set test to pass/fail"""
        
        # set request headers
        for header_name, header_value in self.runner.headers.items():
            self.headers[header_name] = header_value

        # make GET/POST request
        apply_params = self.test.kwargs["apply_params"]
        request_method = REQUEST_METHOD[self.http_method]

        if apply_params == "no":
            response = request_method(self.uri, headers=self.headers)
            self.set_test_status(self.uri, {}, response)
        elif apply_params == "all":
            response = request_method(self.uri, headers=self.headers, 
                                      params=self.params)
            self.set_test_status(self.uri, self.params, response)
        elif apply_params == "cases":
            for key, value in self.params.items():
                param_case = {key: value}
                response = request_method(self.uri, headers=self.headers, 
                                      params=param_case)
                self.set_test_status(self.uri, param_case, response)
    
    def set_test_status(self, uri, params, response):
        # if response is 200, validate against external schema
        # if schema matches instance, test succeeds, otherwise, test fails

        if self.test.result != -1:
            if response.status_code == 200:
                sv = SchemaValidator(self.schema_file)
                validation_result = sv.validate_instance(response.json())
                self.test.result = validation_result["status"]

                helper_text = "<br>Request: " + uri \
                              + "<br>Params: " + str(params) \
                              + "<br>Response: " + response.text

                self.test.set_pass_text(self.test.get_pass_text() + helper_text)
                self.test.set_fail_text(self.test.get_fail_text() + helper_text)

                if validation_result["status"] == -1:
                    self.test.set_fail_text(
                        self.test.get_fail_text()
                        + "<br>Exception: " 
                        + validation_result["exception_class"]
                        + "<br>Message:<br>" + validation_result["message"]
                    )
            else:
                self.test.result = -1