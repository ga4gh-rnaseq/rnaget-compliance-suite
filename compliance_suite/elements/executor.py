# -*- coding: utf-8 -*-
"""Module compliance_suite.elements.executor.py

This module contains the Executor class, which executes all components
and cases for a single test. One Executor is associated with one Node. 
Launches all test cases and stores results as JSON/dict
"""

import requests
import json

from compliance_suite.elements.api_component import APIComponent
from compliance_suite.elements.content_component import ContentComponent
from compliance_suite.elements.element import Element
from compliance_suite.schema_validator import SchemaValidator
from compliance_suite.config.constants import *
import compliance_suite.exceptions.test_status_exception as tse

class Executor(Element):
    """Executes all Test Components and Cases for a single Test/Node

    The Executor is a generalized model for executing all components and
    cases of a single test (API route testing and file content testing).

    Attributes:
        status (int): indicates pass/fail of Test/Node
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    """

    def __init__(self, test, runner):
        """instantiates a Executor object
        
        Args:
            status (int): indicates if test components passed/failed
            test (Node): reference to Node object
            runner (Runner): reference to Runner object
        """

        self.status = 2
        self.test = test
        self.runner = runner

        # Executor only has an API Component if "api" property exists
        # in Node kwargs
        self.api_component = None
        if "api" in test.kwargs.keys():
            self.api_component = APIComponent(
                test.kwargs["api"], self.test, self.runner)
        
        # Executor only has a Content Component if "content" property exists
        # in Node kwargs
        self.content_component = None
        if "content" in test.kwargs.keys():
            self.content_component = ContentComponent(
                test.kwargs["content"], self.test, self.runner)
    
    def execute_tests(self):
        """Execute all test cases for each existing component
        
        Executes api cases if api component exists, and content cases if 
        content component exists. Sets its own status according to the statuses
        of all existing components
        """

        if self.api_component:
            self.api_component.execute_cases()
        if self.content_component:
            self.content_component.execute_cases()
        self.set_status_by_components()
    
    def set_status_by_components(self):
        """Set status according to the status of all components"""

        # status is ONLY 1 (success) if all existing components also have a
        # status of 1. If any component fails, the overall test fails
        status = 1

        if self.api_component:
            if self.api_component.status != 1:
                status = -1
        
        if self.content_component:
            if self.content_component.status != 1:
                status = -1

        self.status = status
    
    def as_json(self):
        """Get all test and component information as JSON/dict

        Returns:
            (dict): JSON object/dict of test and component information
        """

        return {
            "status": self.status,
            "has_api_component": True if self.api_component else False,
            "has_content_component": True if self.content_component else False,
            "api_component": self.api_component.as_json() \
                             if self.api_component else False,
            "content_component": self.content_component.as_json() \
                                 if self.content_component else False
        }
