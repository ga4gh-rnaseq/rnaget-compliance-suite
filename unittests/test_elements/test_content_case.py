# -*- coding: utf-8 -*-
"""Module unittests.test_elements.test_content_case.py"""

from compliance_suite.elements.content_case import ContentCase
from unittests.methods import *

def test_content_case_success():
    success_cases = [
        # {"name": "Expression Get Content 1"},
        # {"name": "Continuous Get Content, Assert Correct Values, 1"},
        {"name": "Continuous Get Content, chr, start, and end, 1"}
    ]

    for success_case in success_cases:
        runner, node, case_params = get_runner_node_case_params_by_case(
            success_case["name"])
        runner.retrieved_server_settings["expressions"]["exp_format"] = "loom"
        runner.retrieved_server_settings["continuous"]["exp_format"] = "loom"
        content_case = ContentCase(case_params, node, runner)
        content_case.execute_test_case()
        assert content_case.status == 1