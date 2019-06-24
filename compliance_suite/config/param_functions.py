import compliance_suite.config.constants as c

def switch_format_param(params):
    if params["format"].lower() == "loom":
        params["format"] = "tsv"
    else:
        params["format"] = "loom"