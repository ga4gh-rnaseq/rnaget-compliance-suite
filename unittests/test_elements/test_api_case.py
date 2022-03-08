# -*- coding: utf-8 -*-
"""Module unittests.test_elements.test_api_case.py"""

from compliance_suite.elements.api_case import APICase
from unittests.methods import *

def test_api_case_success():
    success_cases = [
        {"name": "Get Test Project"},
        {"name": "Search Projects With All Filters"},
        {"name": "Get Test Study"},
        {"name": "Get Test Expression Ticket"},
        {"name": "Get Test Continuous Ticket"}
    ]

    for success_case in success_cases:
        runner, node, case_params = get_runner_node_case_params_by_case(
            success_case["name"])
        api_case = APICase(case_params, node, runner)

        print(case_params)
        print(node)
        print(runner)

        api_case.execute_test_case()
        assert api_case.status == 1

def test_api_case_failure():
    failure_cases = [
        {
            "name": "Get Test Project",
            "replace": {
                "url": "projects/b6b3431e95f6cc6dbc69b0f0bbcb73a3"
            },
            "message": "'mismatchedID3939437e220db196e27b' is not one of "
                + "['9c0eba51095d3939437e220db196e27b']"
        },
        {
            "name": "Get Test Project",
            "replace": {
                "url": "projects/251de42306846bffec4290dca8064cb0"
            },
            "message": "Error parsing JSON from response"
        }
    ]

    for failure_case in failure_cases:
        runner, node, case_params = get_runner_node_case_params_by_case(
            failure_case["name"])
        api_case = APICase(case_params, node, runner)
        api_case.case_params.update(failure_case["replace"])
        api_case.execute_test_case()
        assert api_case.status == -1
        assert api_case.error_message == failure_case["message"]
