import compliance_suite.config.constants as c

def all_supported_filters(test, runner):
    obj_type = test.kwargs["obj_type"]
    obj_id = test.kwargs["obj_instance"]["id"]
    all_filters = c.TEST_RESOURCES[obj_type][obj_id]["filters"]
    supp_filters = runner.retrieved_server_settings[obj_type]["supp_filters"]
    
    filters = {}
    for f in supp_filters:
        if f in all_filters.keys():
            filters[f] = all_filters[f]

    return filters

def single_supported_filter(test, runner, idx):
    filters = all_supported_filters(test, runner)
    sorted_filter_keys = sorted(filters.keys())
    
    fkey = None
    single_filter = {}

    if len(sorted_filter_keys) > 0: 
        if idx < len(sorted_filter_keys):
            fkey = sorted_filter_keys[idx]
        else:
            fkey = sorted_filter_keys[-1]

        single_filter = {fkey: filters[fkey]}
    return single_filter

def first_supported_filter(test, runner):
    return single_supported_filter(test, runner, 0)

def second_supported_filter(test, runner):
    return single_supported_filter(test, runner, 1)

def third_supported_filter(test, runner):
    return single_supported_filter(test, runner, 2)

def incorrect_filter_values(test, runner):
    filters = all_supported_filters(test, runner)
    for k in filters.keys():
        filters[k] = c.NONEXISTENT_ID
    return filters

def add_format_from_retrieved_settings(test, runner):
    filters = {}
    obj_type = test.kwargs["obj_type"]
    filters["format"] = runner.retrieved_server_settings[obj_type]["exp_format"]
    return filters

def all_supported_filters_and_format_from_retrieved_settings(test, runner):
    filters_a = all_supported_filters(test, runner)
    filters_b = add_format_from_retrieved_settings(test, runner)

    filters_a.update(filters_b) 
    return filters_a

def first_supported_filter_and_format(test, runner):
    filters_a = first_supported_filter(test, runner)
    filters_b = add_format_from_retrieved_settings(test, runner)
    filters_a.update(filters_b)
    return filters_a

def second_supported_filter_and_format(test, runner):
    filters_a = second_supported_filter(test, runner)
    filters_b = add_format_from_retrieved_settings(test, runner)
    filters_a.update(filters_b)
    return filters_a

def incorrect_filters_and_format(test, runner):
    filters = all_supported_filters_and_format_from_retrieved_settings(test, runner)
    for k in filters.keys():
        filters[k] = c.NONEXISTENT_ID
    return filters

def switch_format_param(test, runner):
    filters = add_format_from_retrieved_settings(test, runner)
    if filters["format"].lower() == "loom":
        filters["format"] = "tsv"
    else:
        filters["format"] = "loom"
    return filters

def all_supported_filters_format_and_slice_params(content_case):
    test = content_case.test
    runner = content_case.runner
    c = content_case.case_params
    filters = all_supported_filters_and_format_from_retrieved_settings(test, runner)

    slice_params = ["featureIDList", "featureNameList", "sampleIDList"]
    for slice_param in slice_params:
        if slice_param in c.keys():
            filters[slice_param] = ",".join(c[slice_param])
            
    return filters