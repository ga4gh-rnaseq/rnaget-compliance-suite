# -*- coding: utf-8 -*-
"""Module compliance_suite.elements.api_component.py

This module contains the APIComponent class, which executes APICase objects and
informs the Executor of their statuses
"""

from compliance_suite.elements.component import Component
from compliance_suite.elements.api_case import APICase

class APIComponent(Component):
    """Executes API Test Cases and informs the TestExecutor of their statuses"""

    def __init__(self, test_params, test, runner):
        """instantiates an APIComponent object

        Args:
            test_params (dict): global properties and properties for each case
            test (Node): reference to Node object
            runner (Runner): reference to Runner object
        """

        super(APIComponent, self).__init__(test_params, test, runner)
        self.case_class = APICase
        self.test_cases = self.create_test_cases() 
