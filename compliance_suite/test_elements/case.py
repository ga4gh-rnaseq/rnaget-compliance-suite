import json
from compliance_suite.test_elements.test_element import TestElement

class Case(TestElement):

    def __init__(self, case_params, test, runner):
        self.status = 2
        self.headers = {}
        self.case_params = {}
        self.test = test
        self.runner = runner

        self.summary = ""
        self.summary_pass = ""
        self.summary_fail = ""
        self.summary_unknown = "An unhandled exception occurred"

        self.error_message = None
        self.audit = []
        self.set_case_parameters(case_params)

        self.full_message = [
            ["Case", self.case_params["name"]],
            ["Desc", self.case_params["description"]]
        ]

    def get_mature_url(self):
        """Returns full uri for an API route, replacing placeholders with ids

        This method constructs a true API route given server and object
        parameters in the user config file. The base url is added to the
        beginning of the route, and placeholders for project, study, and
        expression ids are replaced with true ids provided.

        Args:
            runner (TestRunner): TestRunner instance associated with this test
            immature_uri (str): uri without base url or placeholders replaced

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

        return mature_url
    
    def set_status(self, status):
        self.status = status
    
    def set_case_parameters(self, case_params):
        for k in case_params.keys():
            self.case_params[k] = case_params[k]

    def get_full_message(self):
        return self.full_message
    
    def as_json(self):
        return {
            "status": self.status,
            "name": self.case_params["name"],
            "description": self.case_params["description"],
            "summary": self.summary,
            "error_message": self.error_message,
            "audit": self.audit
        }

    def set_summary(self):
        if self.status == 1:
            self.summary = self.summary_pass
        elif self.status == -1:
            self.summary = self.summary_fail
        elif self.status == 2:
            self.summary = self.summary_unknown
    
    def set_error_message(self, error_message):
        self.error_message = error_message
    
    def append_audit(self, string):
        self.audit.append(string)