from compliance_suite.test_elements.component import Component
from compliance_suite.test_elements.content_case import ContentCase
from compliance_suite.config.constants import *

class ContentComponent(Component):

    def __init__(self, test_params, test, runner):
        self.status = 2
        self.test_params = test_params
        self.test = test
        self.runner = runner
        self.test_cases = self.__create_test_cases()
        self.full_message = []
    
    def __create_test_cases(self):
        test_cases = []
        
        for case_params in self.test_params["cases"]:

            all_parameters = {k: case_params[k] for k in case_params.keys()}
            all_parameters.update(self.test_params["global_properties"])
                
            test_case = ContentCase(all_parameters, self.test, self.runner)
            test_cases.append(test_case)
        
        return test_cases
    
    def execute_cases(self):
        for test_case in self.test_cases:
            test_case.execute_test_case()
        self.set_status_by_cases()
        self.update_full_message()
    
    def update_full_message(self):
        self.full_message = []
        self.full_message.append(["# Content Test Cases", str(len(self.test_cases))])

        for i in range(0, len(self.test_cases)):
            test_case = self.test_cases[i]
            self.full_message.append(["Content Test Case " + str(i), TEST_STATUS_DICT[test_case.status]])
            self.full_message += test_case.get_full_message()
    
    def set_status_by_cases(self):
        status = 1
        for test_case in self.test_cases:
            if test_case.status != 1:
                status = -1
        
        self.status = status

    def get_full_message(self):
        return self.full_message
