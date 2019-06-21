import compliance_suite.config.constants as c

def schema_expression_search_filetypes_match(params):
    d = {"loom": c.SCHEMA_FILE_EXPRESSION_LOOM_ARRAY_FULL,
         "tsv": c.SCHEMA_FILE_EXPRESSION_TSV_ARRAY_FULL}
    return d[params["format"].lower()]

def schema_expression_search_no_filetype_mismatches(params):
    d = {"loom": c.SCHEMA_FILE_EXPRESSION_LOOM_ARRAY,
         "tsv": c.SCHEMA_FILE_EXPRESSION_TSV_ARRAY}
    return d[params["format"].lower()]