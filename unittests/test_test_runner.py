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

def test_flask():
    response = requests.get("http://localhost:5000/")
    val = response.text
    assert val == "Hello, World!"
