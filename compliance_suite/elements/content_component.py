# -*- coding: utf-8 -*-
"""Module compliance_suite.elements.content_component.py

This module contains the ContentComponent class, which executes ContentCase
objects and informs the Executor of their statuses
"""

from compliance_suite.elements.component import Component
from compliance_suite.elements.content_case import ContentCase

class ContentComponent(Component):
    """Executes Content Cases and informs the TestExecutor of their statuses"""

    def __init__(self, test_params, test, runner):
        """instantiates a ContentComponent object

        Args:
            test_params (dict): global properties and properties for each case
            test (Node): reference to Node object
            runner (Runner): reference to Runner object
        """

        super(ContentComponent, self).__init__(test_params, test, runner)
        self.case_class = ContentCase
        self.test_cases = self.create_test_cases() 
