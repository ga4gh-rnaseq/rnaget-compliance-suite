# -*- coding: utf-8 -*-
"""Module unittests.test_functions.test_schema.py"""

from compliance_suite.functions.schema import *
from unittests.methods import *

runner_p, node_p, case_params_p = get_runner_node_case_params_by_case(
    "Search Projects With All Filters")
runner_p.retrieved_server_settings["projects"]["supp_filters"] = [
    "name", "version"]

runner_e, node_e, case_params_e = get_runner_node_case_params_by_case(
    "Expressions Ticket - All Filters")
runner_e.retrieved_server_settings["expressions"]["supp_filters"] = [
    "studyID", "version"]
runner_e.retrieved_server_settings["expressions"]["exp_format"] = "loom"

runner_c, node_c, case_params_c = get_runner_node_case_params_by_case(
    "Continuous Ticket - All Filters")
runner_c.retrieved_server_settings["continuous"]["supp_filters"] = [
    "studyID", "version"]
runner_c.retrieved_server_settings["continuous"]["exp_format"] = "loom"

def test_schema_require_matching_search_params():

    params = {"name": "RNAgetTestProject0", "version": "1.0"}
    arr_filename = schema_require_matching_search_params(runner_p, node_p,
        params)
    exp_filename = "temp.projects.9c0eba51095d3939437e220db196e27b." \
        + "reqsearchparams.array.json"

    assert arr_filename == exp_filename