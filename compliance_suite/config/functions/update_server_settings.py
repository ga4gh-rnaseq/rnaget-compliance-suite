def update_supported_filters(runner, resource, response_obj):
    for filter_obj in response_obj:
        runner.retrieved_server_settings[resource]["supp_filters"]\
            .append(filter_obj["filter"])

def update_expected_format(runner, resource, response_obj):
    format_str = response_obj["fileType"]
    runner.retrieved_server_settings["expressions"]["exp_format"] = format_str
    # runner.retrieved_server_settings["continuous"]["exp_format"] = format_str

    