# -*- coding: utf-8 -*-
"""Module unittests.unittests_methods.py

This module contains common methods to be accessed by multiple unit testing
modules.
"""

import os
import shutil
from unittests.constants import *
from compliance_suite.config.constants import *
from compliance_suite.config.tests import *
from compliance_suite.node import Node
from compliance_suite.runner import Runner
from compliance_suite.elements.executor import Executor
from compliance_suite.elements.api_case import APICase 

def copy_dict(d):
    """create copy of a dictionary

    Args:
        d (dict): dictionary to copy
    
    Returns:
        c (dict): copied dictionary, can be modified without affecting original
    """

    return {k: d[k] for k in d.keys()}

def copy_list(l):
    """create copy of a list

    Args:
        l (list): list to copy
    
    Returns:
        c (list): copied list, can be modified without affecting original
    """

    return [i for i in l]

def remove_output_dirs():
    all_dirs = [
        {"f": DEFAULT_OUTPUT_DIR, "m": shutil.rmtree},
        {"f": OUTPUT_DIR, "m": shutil.rmtree},
        {"f": DEFAULT_OUTPUT_ARCHIVE, "m": os.remove},
        {"f": OUTPUT_ARCHIVE, "m": os.remove},
    ]

    for d in all_dirs:
        if os.path.exists(d["f"]):
            d["m"](d["f"])

def get_runner_node_case_params_by_case(case_name):
    runner = Runner(SERVER_CONFIG)
    runner.base_tests = runner.initiate_tests()

    nodes_by_test_name = {}
    for base_test in runner.base_tests:
        def add_to_nodes_dict(node_obj):
            for child_node in node_obj.children:
                nodes_by_test_name[str(child_node)] = child_node
                if len(child_node.children) > 0:
                    add_to_nodes_dict(child_node)

        node_obj = base_test[2]
        add_to_nodes_dict(node_obj)

    global_params_by_test_name = {
        k: {
            component_k: TESTS_DICT[k][component_k]["global_properties"]
            for component_k in ["api", "content"] 
            if component_k in TESTS_DICT[k].keys()
        } for k in TESTS_DICT.keys()
    }
    
    case_params_by_case_name = {}
    for k in TESTS_DICT.keys():
        for component_k in ["api", "content"]:
            if component_k in TESTS_DICT[k].keys():
                for case in TESTS_DICT[k][component_k]["cases"]:
                    case_params_by_case_name[case["name"]] = {
                        "params": case,
                        "test": k,
                        "component": component_k
                    }
    req_case = case_params_by_case_name[case_name]
    req_component = req_case["component"]
    req_test_name = req_case["test"]

    all_params = global_params_by_test_name[req_test_name][req_component].copy()
    all_params.update(req_case["params"].copy())
    ret_node = nodes_by_test_name[req_test_name]

    return [runner, ret_node, all_params]
