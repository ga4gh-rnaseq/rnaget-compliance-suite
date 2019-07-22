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
    fkey = sorted_filter_keys[idx]

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

def switch_format_param(params):
    if params["format"].lower() == "loom":
        params["format"] = "tsv"
    else:
        params["format"] = "loom"