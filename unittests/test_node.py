# -*- coding: utf-8 -*-
"""Module unittests.test_node.py

This module contains methods to test the node module via pytest.

Attributes:
    server_config (dict): represents valid server config as from yaml file
    tr (TestRunner): base test runner object to assign tests to
"""

from unittests.constants import *
from unittests.methods import *
from compliance_suite.runner import Runner
from compliance_suite.node import Node

server_config = copy_dict(SERVER_CONFIG)
tr = Runner(server_config)
tr.run_tests()

def test_text():
    """assert pass, skip, fail text is correctly set"""

    test_node = tr.base_tests[0][2].children[0]

    pass_text = test_node.get_pass_text()
    assert pass_text == "Project endpoint implemented by the server"

    fail_text = test_node.get_fail_text()
    assert fail_text == "Project endpoint not implemented by the server"

    skip_text = test_node.get_skip_text()
    assert skip_text == "Project endpoint test skipped"

    generated_skip_text = test_node.generate_skip_text()
    assert generated_skip_text == "project_get is skipped because "

    test_node = tr.base_tests[0][2].children[1].children[0]
    assert test_node.kwargs["name"] == "project_search_url_params_all"

    generated_skip_text = test_node.generate_skip_text()
    assert generated_skip_text.startswith(
        "project_search_url_params_all is skipped because Projects cannot "
        + "be retrieved through the search endpoint"
    )
    
def test_to_echo():
    """assert echo method emits correct text based on test result status"""

    test_node = tr.base_tests[0][2].children[0]
    test_node.result = 2
    assert test_node.to_echo() == 'Unknown error'

    test_node.result = 0
    test_node.set_skip_text('')
    assert test_node.to_echo() == "project_get is skipped because "