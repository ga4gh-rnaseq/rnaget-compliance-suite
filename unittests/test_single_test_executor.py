# -*- coding: utf-8 -*-
"""Module unittests.test_single_test_executor.py

This module contains methods to test the single_test_executor module via pytest.

Attributes:
    uri_project_get_success (str): uri tested for successful project get
    uri_project_get_404 (str): uri tested for project get (404 error result)
    uri_project_get_badschema (str): uri tested for project get (schema failure)
    uri_project_search_url_params_all (str): uri tested for project search
    params_project_search_url_params_all (dict): params for project search
    uri_project_not_implemented (str): simulates project endpoint not implement
    uri_study_not_implemented (str): simulates study endpoint not implement
    uri_expression_not_implemented (str): simulates expr endpoint not implement
"""

from unittests.unittests_constants import *
from unittests.unittests_methods import *
from compliance_suite.config.constants import *
from compliance_suite.config.tests import *
from compliance_suite.tests import Test
from compliance_suite.test_runner import TestRunner
from compliance_suite.single_test_executor import SingleTestExecutor as STE

uri_project_get_success = SERVER_CONFIG["base_url"] \
    + TESTS_DICT["project_get"]["uri"].replace(
        "V_PROJECT_ID",
        SERVER_CONFIG["projects"][0]["id"]
    )

uri_project_get_404 = SERVER_CONFIG["base_url"] \
    + TESTS_DICT["project_get"]["uri"].replace(
        "V_PROJECT_ID",
        SERVER_CONFIG["projects"][1]["id"]
    )

uri_project_get_badschema = SERVER_CONFIG["base_url"] \
    + TESTS_DICT["project_get"]["uri"].replace(
        "V_PROJECT_ID",
        SERVER_CONFIG["projects"][2]["id"]
    )

uri_project_search_url_params_all = SERVER_CONFIG["base_url"] \
    + TESTS_DICT["project_search_url_params_all"]["uri"]

params_project_search_url_params_all = SERVER_CONFIG["projects"][0]["filters"]
params_study_search = SERVER_CONFIG["studies"][0]["filters"]
params_expression_search = SERVER_CONFIG["expressions"][0]["filters"]

uri_project_not_implemented = SERVER_CONFIG["base_url"] + \
    "projects/NA"

uri_study_not_implemented = SERVER_CONFIG["base_url"] + \
    "studies/NA"

uri_expression_not_implemented = SERVER_CONFIG["base_url"] + \
    "expressions/NA"

def get_ste(uri, test_name, params):
    """constructs SingleTestExecutor object based on test and uri

    Args:
        uri (str): uri to be tested
        test_name (str): name of test to be looked up in the tests dictionary
        params (dict): request parameters to be submitted
    
    Returns:
        ste (SingleTestExecutor): ste obj with parameters loaded
    """

    # get the test params from the test dict based on name, then load STE object
    test_config = TESTS_DICT[test_name]
    test_obj = Test(**test_config)
    test_runner_obj = TestRunner(copy_dict(SERVER_CONFIG))
    test_runner_obj.headers["Authorization"] = 'Bearer ' \
                                               + str(SERVER_CONFIG["token"])

    ste = STE(uri, test_config["schema"], test_config["http_method"],
              params, test_obj, test_runner_obj)
    return ste

def test_constructor():
    """assert STE constructor sets parameters correctly"""

    test_config = TESTS_DICT["project_get"]
    test_obj = Test(**test_config)
    test_runner_obj = TestRunner(copy_dict(SERVER_CONFIG))
    params = {}

    uri = uri_project_get_success
    ste = get_ste(uri, "project_get", params)
    assert ste.uri == uri
    assert ste.schema_file == test_config["schema"]
    assert ste.http_method == test_config["http_method"]
    assert ste.params == params

def test_execute_project_get_success():
    """assert valid project get request has success result"""

    ste = get_ste(uri_project_get_success, "project_get", {})
    ste.execute_test()
    assert ste.test.result == 1

def test_execute_project_get_404():
    """assert invalid project get request has fail result"""

    ste = get_ste(uri_project_get_404, "project_get", {})
    ste.execute_test()
    assert ste.test.result == -1

def test_execute_project_get_badschema():
    """assert invalid project get request has fail result"""

    ste = get_ste(uri_project_get_badschema, "project_get", {})
    ste.execute_test()
    assert ste.test.result == -1

def test_execute_project_search_url_params_all():
    """assert valid project search request has success result"""

    ste = get_ste(uri_project_search_url_params_all,
                  "project_search_url_params_all",
                  params_project_search_url_params_all)
    ste.execute_test()
    assert ste.test.result == 1

def test_execute_project_search_url_params_cases():
    """assert valid project search cases request has success result"""

    ste = get_ste(uri_project_search_url_params_all,
                  "project_search_url_params_cases",
                  params_project_search_url_params_all)
    ste.execute_test()
    assert ste.test.result == 1

def test_execute_project_search_filters_out():
    """assert project search endpoint filters out non-matching entries"""

    tname = "project_search_filters_out"
    uri = SERVER_CONFIG["base_url"] \
          + TESTS_DICT[tname]["uri"]
    ste = get_ste(uri, tname, params_project_search_url_params_all)
    ste.execute_test()
    assert ste.test.result == 1

def test_execute_study_search_filters_out():
    """assert study search endpoint filters out non-matching entries"""

    tname = "study_search_filters_out"
    uri = SERVER_CONFIG["base_url"] \
          + TESTS_DICT[tname]["uri"]
    ste = get_ste(uri, tname, params_study_search)
    ste.execute_test()
    assert ste.test.result == 1

def test_execute_expression_search_filters_out():
    """assert expression search endpoint filters out non-matching entries"""

    tname = "expression_search_filters_out"
    uri = SERVER_CONFIG["base_url"] \
          + TESTS_DICT[tname]["uri"]
    ste = get_ste(uri, tname, params_expression_search)
    ste.execute_test()
    assert ste.test.result == 1

def test_execute_not_implemented():
    """assert not implemented endpoint simulations return 501 status"""

    cases = [
        [uri_project_not_implemented, "project_endpoint_not_implemented"],
        [uri_study_not_implemented, "study_endpoint_not_implemented"],
        [uri_expression_not_implemented, "expression_endpoint_not_implemented"]
    ]

    for case in cases:
        ste = get_ste(case[0], case[1], {})
        ste.execute_test()
        assert ste.test.result == 1

def test_json_parse_error():
    """asserts json parse error is raised when response body is not in json"""

    b = "project_get" # modify parameters from project get test
    uri = "emptyresponse"
    ste = get_ste(uri, b, {})
    ste.uri = SERVER_CONFIG["base_url"] + uri
    ste.execute_test()
    assert ste.test.result == -1

def test_custom_media_types():
    """asserts media type error is raised when accept doesn't match response"""

    b = "project_get" # modify parameters from project get test
    uri = uri_project_get_success
    ste = get_ste(uri, b, {})
    ste.test.kwargs["use_default_media_types"] = False
    ste.test.kwargs["test_media_types"] = ["text/plain"]
    ste.set_media_types()
    ste.execute_test()

    assert ste.media_types[0] == "text/plain"
    assert ste.test.result == -1