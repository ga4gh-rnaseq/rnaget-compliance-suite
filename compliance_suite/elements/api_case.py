# -*- coding: utf-8 -*-
"""Module compliance_suite.elements.api_case.py

This module contains the APICase class, which executes a single test case 
against the API/service. An API test case makes a single request to the service,
then checks the response for status code, content type, response body, etc
to assert whether the test case passes requirements.
"""

import os
import re
import requests

import compliance_suite.exceptions.test_status_exception as tse
from compliance_suite.schema_validator import SchemaValidator
from compliance_suite.config.constants import *
from compliance_suite.elements.case import Case
from compliance_suite.functions.general import sanitize_dict

class APICase(Case):
    """Executes a single API-based test case against the service"""

    def __init__(self, case_params, test, runner):
        """instantiates an APICase object

        Args:
            case_params (dict): all parameters/properties for the test case
            test (Node): reference to Node object
            runner (Runner): reference to Runner object
        """

        super(APICase, self).__init__(case_params, test, runner)
        self.__set_test_properties()

    def execute_test_case(self):
        """Test API url, validate response and set test to pass/fail"""

        # make GET/POST request
        url = self.get_mature_url()
        request_method = REQUEST_METHOD[self.case_params["http_method"]]
        response = request_method(
            url,
            headers=self.headers, 
            params=self.params)
        self.set_test_status(url, response)
    
    def set_test_status(self, url, response):
        """Sets test status and messages based on response
        
        After making the API request, this method parses the response object
        and cross-references with the expected output (JSON schema, status code,
        etc). Test results are marked pass/fail/skip, and associated messages
        are added. The 3 steps of validating a single test case are as follows:
        1) validate content type/media type, 2) validate response status code,
        3) validate response body matches correct JSON schema

        Args:
            url (str): requested url
            params (dict): key-value mapping of supplied parameters
            response (Response): response object from the request
        """

        # apply_params = self.test.kwargs["apply_params"]
        
        if self.status != -1:
            self.append_audit("Request: " + url)
            self.append_audit("Params: " + str(sanitize_dict(self.params)))
            self.append_audit("Headers: " + str(sanitize_dict(self.headers)))
            # only add response body if JSON format is expected
            if self.is_json:
                if re.compile("json").search(response.headers["Content-Type"]):
                    self.append_audit("Response Body: " + response.text)

            try:
                # Validation 1, Content-Type, Media Type validation
                # check response content type is in accepted media types
                response_media_type = self.__get_response_media_type(response)
                if not response_media_type in set(self.media_types):
                    raise tse.MediaTypeException(
                        "Response Content-Type '%s'" % response_media_type
                        + " not in request accepted media types: "
                        + str(self.media_types) 
                    )
                
                # Validation 2, Status Code match validation
                # if response code matches expected, validate against JSON
                # schema
                if response.status_code not in self.exp_status:
                    raise tse.StatusCodeException(
                        "Response status code: %s" % str(response.status_code)
                        + " not in expected status code(s): "
                        + str(sorted(list(self.exp_status)))
                    )

                # Validation 3, JSON Schema Validation
                # if JSON schema matches response body, test succeeds
                # if a JSON object can't be parsed from the response body,
                # then catch this error and assign exception

                # if JSON object/dict cannot be parsed from the response body,
                # raise a TestStatusException

                # if endpoint not expected to return JSON (is_json == False),
                # skip this step
                if self.is_json:
                    response_json = None
                    try:
                        response_json = response.json()
                    except ValueError as e:
                        raise tse.JsonParseException(
                            "Error parsing JSON from response")

                    if self.schema_func:
                        self.schema_file = self.case_params["schema_func"](
                            self.runner, self.test, self.params)

                    sv = SchemaValidator(self.schema_file)
                    validation_result = sv.validate_instance(response_json)
                    self.set_status(validation_result["status"])

                    if validation_result["status"] == -1:
                        raise tse.SchemaValidationException(
                            validation_result["message"])
                else:
                    self.set_status(1)

                # update the test runner with settings (supported filters,
                # supported formats) retrieved from the server in the response
                if self.server_settings_update_func:
                    self.server_settings_update_func(
                        self.runner,
                        self.test.kwargs["obj_type"],
                        response_json
                    )

            except tse.TestStatusException as e:
                self.set_status(-1)
                self.set_error_message(str(e))
                self.append_audit(
                    "Exception of class %s encountered" % (
                        str(e.__class__.__name__)))
                self.append_audit("Exception Message: " + str(e))

    def __get_response_media_type(self, response):
        """Get media type from 'Content-Type' field of response header"""

        ct = response.headers["Content-Type"].split(";")[0]
        return ct
    
    def __set_test_properties(self):
        """Set all test case properties"""

        self.__set_expected_status_code()
        self.__set_media_types()
        self.__set_params()
        self.__set_schema()
        self.__set_server_settings_update_func()

    def __set_expected_status_code(self):
        """Set the expected status code for this test case"""
        
        k = "expected_status"
        self.exp_status = \
            set([200]) if k not in self.case_params.keys() \
                       else set(self.case_params[k])
    
    def __set_media_types(self):
        """Set accepted media types and accept header from passed params"""

        self.media_types = []
        # assign accepted media types
        # check if default media types will be used for this test,
        # then add any other test-specific media types
        self.media_types = []
        use_default = \
            True if "use_default_media_types" not in self.case_params.keys() \
            else self.case_params["use_default_media_types"]
        if use_default:
            self.media_types = [a for a in DEFAULT_MEDIA_TYPES]
        add_test_specific = \
            False if "media_types" not in self.case_params.keys() else True
        if add_test_specific:
            self.media_types += \
                [a for a in self.case_params["media_types"]]
        self.headers["Accept"] = ", ".join(self.media_types) + ";"

    def __set_params(self):
        """Set request parameters for this test case"""

        self.params = {}
        if "request_params" in self.case_params.keys():
            self.params.update(self.case_params["request_params"])
        if "request_params_func" in self.case_params.keys():
            self.params.update(self.case_params["request_params_func"](
                self.test, self.runner))
    
    def __set_schema(self):
        """Set JSON schema file to check against response body for this case"""

        self.schema_file = None
        self.schema_func = None
        self.is_json = True

        if "schema_file" in self.case_params.keys():
            self.schema_file = self.case_params["schema_file"]
        else:
            self.schema_func = self.case_params["schema_func"]
        
        if "is_json" in self.case_params.keys():
            self.is_json = self.case_params["is_json"]
    
    def __set_server_settings_update_func(self):
        """Set function to update server settings from response data"""

        self.server_settings_update_func = None
        if "server_settings_update_func" in self.case_params.keys():
            self.server_settings_update_func = \
                self.case_params["server_settings_update_func"]
