# -*- coding: utf-8 -*-
"""Module compliance_suite.functions.update_server_settings.py

Functions to update server config/settings based on the response of a previous 
API request. Each function should accept a Runner object and modify its
"retrieved_server_settings" attribute
"""

def update_supported_filters(runner, resource, response_obj):
    """Update server settings with the supported filters for a resource
    
    Arguments:
        runner (Runner): reference to Runner object
        resource (str): identifies project, study, expression, continuous
        response_obj (Response): response object to parse
    """

    for filter_obj in response_obj:
        runner.retrieved_server_settings[resource]["supp_filters"]\
            .append(filter_obj["filter"])

def update_expected_format(runner, resource, response_obj):
    """Update server settings with the expected file format for a resource

    Arguments:
        runner (Runner): reference to Runner object
        resource (str): identifies project, study, expression, continuous
        response_obj (Response): response object to parse
    """

    format_str = response_obj["fileType"]
    runner.retrieved_server_settings["expressions"]["exp_format"] = format_str
    runner.retrieved_server_settings["continuous"]["exp_format"] = format_str

    