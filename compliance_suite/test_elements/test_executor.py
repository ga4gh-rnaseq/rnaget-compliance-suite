# -*- coding: utf-8 -*-
"""Module compliance_suite.test_components.test_executor.py

This module contains class definition for generalized model of testing an api
route. The SingleTestExecutor executes a request, checks status code of the
response, validates the schema of the returned JSON object against the
corresponding schema, and sets the test result to 1 (success) or -1 (fail)

Todo:
    * handle query parameters
    * handle tests for not OK (!=200) response codes
"""

import requests
import json

from compliance_suite.test_elements.api_component import APIComponent
from compliance_suite.test_elements.content_component import ContentComponent
from compliance_suite.schema_validator import SchemaValidator
from compliance_suite.config.constants import *
import compliance_suite.exceptions.test_status_exception as tse

class TestExecutor(object):
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
        media_types (list): all accepted media types
        headers (dict): key, value mapping of request header
        full_message (list): lists associated information with the api test,
            to be assigned to Test object and displayed in report under case
    """

    def __init__(self, test, runner):
        """instantiates a SingleTestExecutor object
        
        Args:
            uri (str): uri to be requested
            test (Test): reference to Test object
            runner (TestRunner): reference to TestRunner object
        """

        self.status = 2
        self.test = test
        self.runner = runner
        self.full_message = []

        self.api_component = None
        if "api" in test.kwargs.keys():
            self.api_component = APIComponent(test.kwargs["api"], self.test, self.runner)
        
        self.content_component = None
        if "content" in test.kwargs.keys():
            self.content_component = ContentComponent(test.kwargs["content"], self.test, self.runner)
        
        # self.__set_test_properties()
    
    def execute_tests(self):
        if self.api_component:
            self.api_component.execute_cases()
        if self.content_component:
            self.content_component.execute_cases()
        self.set_status_by_components()
        self.update_full_message()
    
    def update_full_message(self):
        self.full_message = []

        if self.api_component:
            self.full_message.append(["API Tests"])
            self.full_message += self.api_component.get_full_message()
        if self.content_component:
            self.full_message.append(["Content Tests"])
            self.full_message += self.content_component.get_full_message()
    
    def set_status_by_components(self):
        status = 1

        if self.api_component:
            if self.api_component.status != 1:
                status = -1
        
        if self.content_component:
            if self.content_component.status != 1:
                status = -1

        self.status = status
    
    def get_full_message(self):
        return self.full_message
    
    def as_json(self):
        return {
            "status": self.status,
            "has_api_component": True if self.api_component else False,
            "has_content_component": True if self.content_component else False,
            "api_component": self.api_component.as_json() if self.api_component else False,
            "content_component": self.content_component.as_json() if self.content_component else False
        }
