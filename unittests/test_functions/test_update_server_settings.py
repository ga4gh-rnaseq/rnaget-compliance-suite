# -*- coding: utf-8 -*-
"""Module unittests.test_functions.test_update_server_settings.py"""

import json

from compliance_suite.functions.update_server_settings import *
from unittests.methods import *

def test_update_supported_filters():
    runner_p, node_p, case_params_p = get_runner_node_case_params_by_case(
        "Search Projects With All Filters")

    response_obj = [
        {
            "fieldType": "string",
            "filter": "version",
            "description": "version to search for"
        },
        {
            "fieldType": "string",
            "filter": "name",
            "description": "name of project"
        },
        {
            "fieldType": "string",
            "filter": "tags",
            "description": "tags associated with project"
        }
    ]

    update_supported_filters(runner_p, "projects", response_obj)
    filters_l = runner_p.retrieved_server_settings["projects"]["supp_filters"]

    assert len(filters_l) == 3
    assert "version" in set(filters_l)
    assert "name" in set(filters_l)
    assert "tags" in set(filters_l)
