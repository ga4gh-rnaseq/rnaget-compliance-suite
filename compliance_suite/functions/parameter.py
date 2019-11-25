# -*- coding: utf-8 -*-
"""Module compliance_suite.functions.parameter.py

Functions to assign request parameters according to test case. Each function
in this module should return a dictionary of key,value parameters to pass to 
the request function
"""

import json
import compliance_suite.config.constants as c

def all_supported_filters(test, runner):
    """Get all filter parameters the server supports
    
    Uses the runner's retrieved server settings to produce a full set of 
    parameters supported by the server

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    Returns:
        (dict): request filters
    """

    # get all potential filters, and all filter names the server supports
    obj_type = test.kwargs["obj_type"]
    obj_id = test.kwargs["obj_instance"]["id"]
    all_filters = c.TEST_RESOURCES[obj_type][obj_id]["filters"]
    supp_filters = runner.retrieved_server_settings[obj_type]["supp_filters"]
    
    # return only the filter name/values the server supports as a dict
    filters = {}
    for f in supp_filters:
        if f in all_filters.keys():
            filters[f] = all_filters[f]

    return filters

def single_supported_filter(test, runner, idx):
    """Get a single filter supported by the server

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
        idx (int): single filter to retrieve by its index

    Returns:
        (dict): single request filter
    """

    # get all supported filters and sort filter keys
    filters = all_supported_filters(test, runner)
    sorted_filter_keys = sorted(filters.keys())
    
    fkey = None
    single_filter = {}

    # get single filter by the key's position in the sorted list
    # if there is no filter at the index, get the last element in the list
    if len(sorted_filter_keys) > 0: 
        if idx < len(sorted_filter_keys):
            fkey = sorted_filter_keys[idx]
        else:
            fkey = sorted_filter_keys[-1]

        single_filter = {fkey: filters[fkey]}

    return single_filter

def first_supported_filter(test, runner):
    """Get the first filter supported by the server

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): single (first) request filter
    """

    return single_supported_filter(test, runner, 0)

def second_supported_filter(test, runner):
    """Get the second filter supported by the server

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object

    Returns:
        (dict): single (second) request filter
    """

    return single_supported_filter(test, runner, 1)

def third_supported_filter(test, runner):
    """Get the third filter supported by the server

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object

    Returns:
        (dict): single (third) request filter
    """

    return single_supported_filter(test, runner, 2)

def incorrect_filter_values(test, runner):
    """Replace all supported filters with an incorrect value
    
    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): supported filters, with values made incorrect
    """

    # replace each supported filter with the nonexistent id
    filters = all_supported_filters(test, runner)
    for k in filters.keys():
        filters[k] = c.NONEXISTENT_ID
    return filters

def add_format_from_retrieved_settings(test, runner):
    """Get format from server settings and make it a request parameter/filter

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): filter dictionary specifying requested file format
    """

    filters = {}
    obj_type = test.kwargs["obj_type"]
    filters["format"] = runner.retrieved_server_settings[obj_type]["exp_format"]
    return filters

def all_supported_filters_and_format_from_retrieved_settings(test, runner):
    """Get all supported filters and format as parameter dictionary

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): filter dictionary of all supported filters plus format
    """

    filters_a = all_supported_filters(test, runner)
    filters_b = add_format_from_retrieved_settings(test, runner)
    filters_a.update(filters_b)

    return filters_a

def first_supported_filter_and_format(test, runner):
    """Get the first filter supported by server and format

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): first request filter plus format
    """

    filters_a = first_supported_filter(test, runner)
    filters_b = add_format_from_retrieved_settings(test, runner)
    filters_a.update(filters_b)
    return filters_a

def second_supported_filter_and_format(test, runner):
    """Get the second filter supported by server and format

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): second request filter plus format
    """

    filters_a = second_supported_filter(test, runner)
    filters_b = add_format_from_retrieved_settings(test, runner)
    filters_a.update(filters_b)
    return filters_a

def incorrect_filters_and_format(test, runner):
    """Get the third filter supported by server and format

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): third request filter plus format
    """

    filters = all_supported_filters_and_format_from_retrieved_settings(
        test, runner)
    for k in filters.keys():
        filters[k] = c.NONEXISTENT_ID
    return filters

def switch_format_param(test, runner):
    """Get a different format than what is expected according to server settings

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): format specified, but modified from server settings
    """

    filters = add_format_from_retrieved_settings(test, runner)
    if filters["format"].lower() == "loom":
        filters["format"] = "tsv"
    else:
        filters["format"] = "loom"
    return filters

def expression_slice_params(content_case):
    c = content_case.case_params
    slice_params = ["featureIDList", "featureNameList", "sampleIDList"]
    filters = {}
    for slice_param in slice_params:
        if slice_param in c.keys():
            filters[slice_param] = ",".join(c[slice_param])
    return filters

def all_supported_filters_format_and_slice_params(content_case):
    """Get supported filters, format, and matrix slicing parameters

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): supported filters, format, and matrix slicing parameters
    """

    test = content_case.test
    runner = content_case.runner
    c = content_case.case_params
    filters = all_supported_filters_and_format_from_retrieved_settings(
        test, runner)

    # for the 3 slice params, convert the list outlined in the tests dict
    # to a comma-separated list
    slice_params = ["featureIDList", "featureNameList", "sampleIDList"]
    for slice_param in slice_params:
        if slice_param in c.keys():
            filters[slice_param] = ",".join(c[slice_param])
    
    # for the 2 threshold params, convert the objects outlined in the tests
    # dict to JSON objects that can be sent in the request
    expression_params = ["minExpression", "maxExpression"]
    for expression_param in expression_params:
        if expression_param in c.keys():
            filters[expression_param] = json.dumps(c[expression_param])
            
    return filters

def chr_start_end(content_case):
    """Get chr, start, end continuous matrix slicing parameters

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): filters for continuous subsetting
    """

    test = content_case.test
    runner = content_case.runner
    c = content_case.case_params
    filters = {}

    # for the 3 slice params, convert the list outlined in the tests dict
    # to a comma-separated list
    continuous_params = ["chr", "start", "end"]
    for continuous_param in continuous_params:
        if continuous_param in c.keys():
            filters[continuous_param] = c[continuous_param]
            
    return filters

def all_supported_filters_format_chr_start_end(content_case):
    """Get supported filters, format, and continuous matrix slicing parameters

    Arguments:
        test (Node): reference to Node object
        runner (Runner): reference to Runner object
    
    Returns:
        (dict): supported filters, format, and continuous slice parameters
    """
    
    test = content_case.test
    runner = content_case.runner
    c = content_case.case_params
    
    filters_a = all_supported_filters_and_format_from_retrieved_settings(
        test, runner)
    filters_b = chr_start_end(content_case)
    filters_a.update(filters_b)

    return filters_a