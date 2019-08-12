# -*- coding: utf-8 -*-
"""Module unittests.test_functions.test_schema.py"""

from compliance_suite.functions.schema import *
from unittests.methods import *

runner_p, node_p, case_params_p = get_runner_node_case_params_by_case(
    "Search Projects With All Filters")
runner_p.retrieved_server_settings["projects"]["supp_filters"] = [
    "name", "version"]

runner_e, node_e, case_params_e = get_runner_node_case_params_by_case(
    "Search Expressions With All Filters")
runner_e.retrieved_server_settings["expressions"]["supp_filters"] = [
    "studyID", "version"]
runner_e.retrieved_server_settings["expressions"]["exp_format"] = "loom"

runner_c, node_c, case_params_c = get_runner_node_case_params_by_case(
    "Search Continuous With All Filters")
runner_c.retrieved_server_settings["continuous"]["supp_filters"] = [
    "studyID", "version"]
runner_c.retrieved_server_settings["continuous"]["exp_format"] = "loom"

def test_get_temp_filename():

    template_filename = "rnaget-project.json"
    value = "1"
    temp_filename = get_temp_filename(template_filename, value)

    assert temp_filename == "temp.rnaget-project-1.json"

def test_schema_expression_search_format():

    params = {"format": "loom"}
    arr_filename = schema_expression_search_format(params)
    exp_filename = "temp.rnaget-expression-array-format-template-loom.json"
    assert arr_filename == exp_filename

def test_schema_expression_search_filetypes_match():

    params = {"format": "loom"}
    arr_filename = schema_expression_search_filetypes_match(runner_e, node_e,
        params)
    exp_filename = "temp.rnaget-expression-array-format-template-loom.json"
    assert arr_filename == exp_filename

def test_schema_expression_search_no_filetype_mismatches():

    params = {"format": "tsv"}
    arr_filename = schema_expression_search_no_filetype_mismatches(runner_e,
        node_e, params)
    exp_filename = "temp.rnaget-expression-array-format-template-tsv.json"
    assert arr_filename == exp_filename

def test_schema_continuous_search_format():

    params = {"format": "tsv"}
    arr_filename = schema_continuous_search_format(params)
    exp_filename = "temp.rnaget-continuous-array-format-template-tsv.json"
    assert arr_filename == exp_filename

def test_schema_continuous_search_filetypes_match():

    params = {"format": "loom"}
    arr_filename = schema_continuous_search_filetypes_match(runner_c, node_c,
        params)
    exp_filename = "temp.rnaget-continuous-array-format-template-loom.json"
    assert arr_filename == exp_filename

def test_schema_continuous_search_no_filetype_mismatches():

    params = {"format": "loom"}
    arr_filename = schema_continuous_search_no_filetype_mismatches(runner_c,
        node_c, params)
    exp_filename = "temp.rnaget-continuous-array-format-template-loom.json"
    assert arr_filename == exp_filename

def test_schema_require_matching_search_params():

    params = {"name": "RNAgetTestProject0", "version": "1.0"}
    arr_filename = schema_require_matching_search_params(runner_p, node_p,
        params)
    exp_filename = "temp.projects.9c0eba51095d3939437e220db196e27b." \
        + "reqsearchparams.array.json"

    assert arr_filename == exp_filename