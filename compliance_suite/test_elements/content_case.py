# -*- coding: utf-8 -*-
"""Module compliance_suite.content_case.py

This module contains the ContentCase class, which asserts that file attachments
returned by the API match expected output. A Content test case generally 
makes a request to the service for an expression or continuous matrix, then
downloads the file attachment located at the server-specified 'URL'.
"""

import requests
import compliance_suite.exceptions.test_status_exception as tse

from compliance_suite.schema_validator import SchemaValidator
from compliance_suite.config.constants import *
from compliance_suite.test_elements.case import Case

class ContentCase(Case):
    """A single test case to assert file attachment matches expected output"""

    def __init__(self, case_params, test, runner):
        """instantiates a ContentCase object"""

        super(ContentCase, self).__init__(case_params, test, runner)

    def execute_test_case(self):
        """Execute the test case function and update status"""

        case_result = self.case_params["function"](self)
        self.set_status(case_result["status"])
        return case_result
