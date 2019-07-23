import requests

import compliance_suite.exceptions.test_status_exception as tse
from compliance_suite.schema_validator import SchemaValidator
from compliance_suite.config.constants import *
from compliance_suite.test_elements.case import Case

class ContentCase(Case):
    def __init__(self, case_params, test, runner):
        super(ContentCase, self).__init__(case_params, test, runner)

    def set_status(self, status):
        self.status = status

    def set_case_parameters(self, case_params):
        for k in case_params.keys():
            self.case_params[k] = case_params[k]
    
    def get_full_message(self):
        return self.full_message

    def execute_test_case(self):
        case_result = self.case_params["function"](self)
        self.status = case_result["status"]
        self.full_message.append(case_result["message"])
        return case_result