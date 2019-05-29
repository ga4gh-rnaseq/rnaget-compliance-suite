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

def get_ste(uri, test_name, params):
    test_config = TESTS_DICT[test_name]
    test_obj = Test(**test_config)
    test_runner_obj = TestRunner(copy_dict(SERVER_CONFIG))
    test_runner_obj.headers["Authorization"] = 'Bearer ' \
                                               + str(SERVER_CONFIG["token"])

    ste = STE(uri, test_config["schema"], test_config["http_method"],
              params, test_obj, test_runner_obj)
    return ste

def test_constructor():
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
    assert ste.headers == ACCEPT_HEADER

def test_execute_project_get_success():
    ste = get_ste(uri_project_get_success, "project_get", {})
    ste.execute_test()
    assert ste.test.result == 1

def test_execute_project_get_404():
    ste = get_ste(uri_project_get_404, "project_get", {})
    ste.execute_test()
    assert ste.test.result == -1

def test_execute_project_get_badschema():
    ste = get_ste(uri_project_get_badschema, "project_get", {})
    ste.execute_test()
    assert ste.test.result == -1

def test_execute_project_search_url_params_all():
    ste = get_ste(uri_project_search_url_params_all,
                  "project_search_url_params_all",
                  params_project_search_url_params_all)
    ste.execute_test()
    assert ste.test.result == 1

def test_execute_project_search_url_params_cases():
    ste = get_ste(uri_project_search_url_params_all,
                  "project_search_url_params_cases",
                  params_project_search_url_params_all)
    ste.execute_test()
    assert ste.test.result == -1
