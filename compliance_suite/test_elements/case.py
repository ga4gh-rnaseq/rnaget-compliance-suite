from compliance_suite.test_elements.test_element import TestElement

class Case(TestElement):

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