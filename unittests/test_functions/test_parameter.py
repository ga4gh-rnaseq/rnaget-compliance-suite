# -*- coding: utf-8 -*-
"""Module unittests.test_functions.test_attribte_handlers.py"""

from compliance_suite.functions.parameter import *
from unittests.methods import *

import compliance_suite.config.constants as c

runner_p, node_p, case_params_p = get_runner_node_case_params_by_case(
    "Search Projects With All Filters")
runner_p.retrieved_server_settings["projects"]["supp_filters"] = [
    "version", "name"]

runner_e, node_e, case_params_e = get_runner_node_case_params_by_case(
    "Search Expressions With All Filters")
runner_e.retrieved_server_settings["expressions"]["supp_filters"] = [
    "studyID", "version"]
runner_e.retrieved_server_settings["expressions"]["exp_format"] = "loom"

runner_c, node_c, case_params_c = get_runner_node_case_params_by_case(
    "Search Continuous With All Filters")
runner_e.retrieved_server_settings["continuous"]["supp_filters"] = [
    "studyID", "version"]
runner_e.retrieved_server_settings["continuous"]["exp_format"] = "tsv"

def test_all_supported_filters():
    
    filters = all_supported_filters(node_p, runner_p)
    assert filters["version"] == "1.0"
    assert filters["name"] == "RNAgetTestProject0"

def test_first_supported_filter():

    filters = first_supported_filter(node_p, runner_p)
    assert len(filters) == 1
    assert filters["name"] == "RNAgetTestProject0"

def test_second_supported_filter():

    filters = second_supported_filter(node_p, runner_p)
    assert len(filters) == 1
    assert filters["version"] == "1.0"

def test_third_supported_filter():

    filters = third_supported_filter(node_p, runner_p)
    assert len(filters) == 1
    assert filters["version"] == "1.0"

def test_incorrect_filter_values():

    filters = incorrect_filter_values(node_p, runner_p)
    assert filters["name"] == c.NONEXISTENT_ID
    assert filters["version"] == c.NONEXISTENT_ID


def test_add_format_from_retrieved_settings():

    filters = add_format_from_retrieved_settings(node_e, runner_e)
    assert len(filters) == 1
    assert filters["format"] == "loom"

def test_all_supported_filters_and_format_from_retrieved_settings():

    filters = all_supported_filters_and_format_from_retrieved_settings(
        node_e, runner_e)
    assert filters["format"] == "loom"
    assert filters["version"] == "1.0"
    assert filters["studyID"] == "f3ba0b59bed0fa2f1030e7cb508324d1"

def test_first_supported_filter_and_format():

    filters = first_supported_filter_and_format(node_e, runner_e)
    assert len(filters) == 2
    assert filters["format"] == "loom"
    assert filters["studyID"] == "f3ba0b59bed0fa2f1030e7cb508324d1"

def test_second_supported_filter_and_format():

    filters = second_supported_filter_and_format(node_e, runner_e)
    assert len(filters) == 2
    assert filters["format"] == "loom"
    assert filters["version"] == "1.0"

def test_incorrect_filters_and_format():
    
    filters = incorrect_filters_and_format(node_e, runner_e)
    assert filters["format"] == c.NONEXISTENT_ID
    assert filters["studyID"] == c.NONEXISTENT_ID

def test_switch_format_param():

    filters = switch_format_param(node_e, runner_e)
    assert filters["format"] == "tsv"
    filters = switch_format_param(node_c, runner_c)
    assert filters["format"] == "loom"

def test_all_supported_filters_format_and_slice_params():
    pass