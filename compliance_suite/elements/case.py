# -*- coding: utf-8 -*-
"""Module compliance_suite.elements.case.py

This module contains the Case class, an abstract representation of a 
Test Case. A Component holds many Cases, cases are generally distinguished as
a single API call or function, and associated assertions to check for an 
expected outcome. 
"""

import json
from compliance_suite.elements.element import Element

class Case(Element):
    """Abstract representation of a test case

    Attributes:
        status (int) indicates pass/fail of Case
        case_params (dict): properties needed to execute and assert status
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
        headers (dict): headers used in HTTP request
        summary (str): summary message for this test case in report
        potential_summaries (dict): different summary messages based on the
            test case outcome. One of these will be the final summary
        error_message (str): output in the report if case fails
        audit (list): audit log of the test case, output in the report, for
            debugging
    """

    def __init__(self, case_params, test, runner):
        """instantiates a Case object

        Args:
            case_params (dict): all parameters/properties for the test case
            test (Node): reference to Node object
            runner (Runner): reference to Runner object
        """

        self.status = 2
        self.case_params = {}
        self.set_case_parameters(case_params)
        self.test = test
        self.runner = runner

        # set request headers
        self.headers = {}
        for header_name, header_value in self.runner.headers.items():
            self.headers[header_name] = header_value

        # set current summary and potential summaries
        self.summary = ""
        self.potential_summaries = {
            1: self.case_params["summary_pass"] \
               if "summary_pass" in self.case_params.keys() else "",
            -1: self.case_params["summary_fail"] \
                if "summary_fail" in self.case_params.keys() else "",
            0: self.case_params["summary_skip"] \
               if "summary_skip" in self.case_params.keys() else "",
            2: "An unhandled exception occurred"
        }
        self.summary = self.set_summary()

        self.error_message = None
        self.audit = []

    def get_mature_url(self):
        """Returns full uri for an API route, replacing placeholders with ids

        This method constructs a true API route given server and object
        parameters in the user config file. The base url is added to the
        beginning of the route, and placeholders for project, study, and
        expression ids are replaced with true ids provided.

        Returns:
            (str): mature uri with base url added and placeholders replaced
        """

        mature_url = self.runner.server_config["base_url"]

        obj_type_placeholders = {
            "projects": "V_PROJECT_ID",
            "studies": "V_STUDY_ID",
            "expressions": "V_EXPRESSION_ID",
            "continuous": "V_CONTINUOUS_ID"
        }

        mature_url += self.case_params["url"].replace(
            obj_type_placeholders[self.test.kwargs["obj_type"]],
            self.test.kwargs["obj_instance"]["id"]
        )

        return mature_url.rstrip("/")
    
    def set_status(self, status):
        """Set test case status"""

        self.status = status
    
    def set_case_parameters(self, case_params):
        """Set parameters/properties for test case
        
        Arguments:
            case_params (dict): case parameters
        """

        for k in case_params.keys():
            self.case_params[k] = case_params[k]
    
    def set_summary(self):
        """Set summary message for test case"""

        self.summary = self.potential_summaries[self.status]
    
    def set_error_message(self, error_message):
        """Set error message for test case"""

        self.error_message = error_message
    
    def as_json(self):
        """Get information for this test case as JSON/dict"""
        
        self.set_summary()

        return {
            "status": self.status,
            "name": self.case_params["name"],
            "description": self.case_params["description"],
            "summary": self.summary,
            "error_message": self.error_message,
            "audit": self.audit
        }
    
    def append_audit(self, string):
        """Add a message to the test case audit log

        Arguments:
            string (str): message to add to audit log
        """

        self.audit.append(string)