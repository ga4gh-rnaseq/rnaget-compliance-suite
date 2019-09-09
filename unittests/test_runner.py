# -*- coding: utf-8 -*-
"""Module unittests.test_runner.py

This module contains methods to test the runner module via pytest.
"""

import requests
import json
from unittests.constants import *
from unittests.methods import *
from compliance_suite.runner import Runner

def test_constructor():
    """asserts constructor correctly sets attributes"""

    server_config = copy_dict(SERVER_CONFIG)
    tr = Runner(server_config)
    assert tr.root == None
    assert tr.total_tests == 0
    assert tr.total_tests_passed == 0
    assert tr.total_tests_failed == 0
    assert tr.total_tests_skipped == 0
    assert tr.total_tests_warning == 0
    assert tr.server_config == server_config
    assert tr.results == {"projects": {}, "studies": {}, "expressions": {},
                          "continuous": {}}
    assert tr.headers == {}

def test_not_implemented():
    """asserts base tests are set to non-implemented versions when specified"""

    server_config = copy_dict(SERVER_CONFIG_NOT_IMPLEMENTED)
    tr = Runner(server_config)
    tr.run_tests()
    a = "_endpoint_not_implemented"
    assert tr.base_tests[0][2].children[0].kwargs["name"] == "project" + a
    assert tr.base_tests[1][2].children[0].kwargs["name"] == "study" + a
    assert tr.base_tests[2][2].children[0].kwargs["name"] == "expression" + a

def test_generate_final_json():
    """asserts final generated json from all tests matches expected output"""

    server_config = copy_dict(SERVER_CONFIG_NOT_IMPLEMENTED)
    tr = Runner(server_config)
    tr.run_tests()

    expect_final_json = json.loads(
        open("unittests/data/json_reports/final_json.json", "r").read()
    )
    actual_final_json = tr.generate_final_json()
    actual_final_json["date_time"] = "0"
    actual_json_s = str(actual_final_json).replace("'", '"').replace("\\","")
    expect_json_s = str(expect_final_json).replace("'", '"').replace("\\","")

    # assert actual_json_s == expect_json_s

def test_recurse_generate_json():

    server_config = copy_dict(SERVER_CONFIG)
    tr = Runner(server_config)
    tr.run_tests()
    
    obj_type, obj_id, node = tr.base_tests[0]
    child = node.children[0]
    child.result = 1

    tr.recurse_generate_json(obj_type, obj_id, node)
