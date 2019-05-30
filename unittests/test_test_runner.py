import requests
from unittests.unittests_constants import *
from unittests.unittests_methods import *
from compliance_suite.test_runner import TestRunner


def test_constructor():
    server_config = copy_dict(SERVER_CONFIG)
    tr = TestRunner(server_config)
    assert tr.root == None
    assert tr.session_params == {}
    assert tr.total_tests == 0
    assert tr.total_tests_passed == 0
    assert tr.total_tests_failed == 0
    assert tr.total_tests_skipped == 0
    assert tr.total_tests_warning == 0
    assert tr.server_config == server_config
    assert tr.results == {"projects": {}, "studies": {}, "expressions": {}}
    assert tr.headers == {}

def test_not_implemented():
    server_config = copy_dict(SERVER_CONFIG_NOT_IMPLEMENTED)
    tr = TestRunner(server_config)
    tr.run_tests()
    a = "_endpoint_not_implemented"
    assert tr.base_tests[0][2].children[0].kwargs["name"] == "project" + a
    assert tr.base_tests[1][2].children[0].kwargs["name"] == "study" + a
    assert tr.base_tests[2][2].children[0].kwargs["name"] == "expression" + a

def test_flask():
    response = requests.get("http://localhost:5000/")
    val = response.text
    assert val == "Hello, World!"
