import requests

from compliance_suite.schema_validator import SchemaValidator
from compliance_suite.config.constants import *

class SingleTestExecutor(object):

    def __init__(self, uri, schema_file, http_method, params, test, runner):
        self.uri = uri
        self.schema_file = schema_file
        self.http_method = http_method
        self.params = params
        self.test = test
        self.runner = runner
        self.headers = ACCEPT_HEADER
    
    def execute_test(self):
        
        for header_name, header_value in self.runner.headers.items():
            self.headers[header_name] = header_value
        response = REQUEST_METHOD[self.http_method](
            self.uri,
            headers=self.headers,
            params=self.params
        )

        if response.status_code == 200:
            sv = SchemaValidator(self.schema_file)
            validation_result = sv.validate_instance(response.json())
            self.test.result = validation_result["status"]

            if validation_result["status"] == -1:
                self.test.set_fail_text(
                    self.test.get_fail_text()
                    + "<br>Exception: " + validation_result["exception_class"]
                    + "<br>Message:<br>" + validation_result["message"]
                )
        else:
            self.test.result = -1