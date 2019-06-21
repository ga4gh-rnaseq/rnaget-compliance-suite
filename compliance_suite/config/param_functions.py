import compliance_suite.config.constants as c

def switch_format_param(params):
    d = {"loom": "tsv", "LOOM": "TSV", "tsv": "loom", "TSV": "LOOM"}
    params["format"] = d[params["format"]]