# -*- coding: utf-8 -*-
"""Module compliance_suite.elements.component.py

This module contains the Component class, an abstract representation of a 
Test Component. A Test can hold one or more Components, components are 
distinguished by theme. eg. one component tests the API (params, status codes,
response body), whereas another component tests the contents of file 
attachments. A component holds multiple Cases.
"""

from compliance_suite.elements.element import Element
import json

class Component(Element):
    """Abstract representation of a test component
    
    Attributes:
        status (int): indicates pass/fail of Component
        test_params (dict): global properties and properties for each case
        test (Node): reference to Node object
        runner (Node): reference to Runner object
        case_class (class): Test Case class this component will instantiate
    """

    def __init__(self, test_params, test, runner):
        """instantiates a Component object
        
        Args:
            test_params (dict): global properties and properties for each case
            test (Node): reference to Node object
            runner (Runner): reference to Runner object
        """

        self.status = 2
        self.test_params = test_params
        self.test = test
        self.runner = runner
        self.case_class = None
    
    def create_test_cases(self):
        """Create all test cases from params

        For each test case listed in test_params, instantiate a case object
        according to the class in case_class. Each case gets all of global
        properties, as well as the specific properties unique to that case

        Returns:
            (list): All test cases, as objects of class referenced in case_class
        """

        test_cases = []
        
        for case_params in self.test_params["cases"]:

            global_params = self.test_params["global_properties"].copy()
            case_params = case_params.copy()

            all_params = {}
            all_params.update(global_params)
            all_params.update(case_params)
                
            test_case = self.case_class(all_params, self.test, self.runner)
            test_cases.append(test_case)
        
        return test_cases

    def execute_cases(self):
        """Executes all test cases and sets status according to case results"""

        for test_case in self.test_cases:
            test_case.execute_test_case()
        self.set_status_by_cases()
    
    def set_status_by_cases(self):
        """Set status according to the status of all cases"""

        # status is ONLY 1 (success) if all cases also have a status of 1.
        # if any case fails, the overall component fails

        status = 1
        for test_case in self.test_cases:
            if test_case.status != 1:
                status = -1
        
        self.status = status
    
    def as_json(self):
        """Get all test case information as JSON/dict

        Returns:
            (dict): JSON object/dict of information for all test cases
        """

        return {
            "status": self.status,
            "cases": [c.as_json() for c in self.test_cases]
        }