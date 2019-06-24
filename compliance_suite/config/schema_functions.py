import compliance_suite.config.constants as c
import compliance_suite.schema_validator as sv
import os

def render_and_write_temp_schema(output_filename, template, replace_l):
     schema_dir = os.path.dirname(sv.__file__) \
                     + "/" + c.SCHEMA_RELATIVE_DIR
     template_file = schema_dir + "/" + template
     json = open(template_file, "r").read()
     for replace in replace_l:
          json = json.replace(replace[0], replace[1])
     out_path = schema_dir + "/" + output_filename
     open(out_path, "w").write(json)

def schema_expression_search_filetypes_match(params):
    d = {"loom": c.SCHEMA_FILE_EXPRESSION_LOOM_ARRAY_FULL,
         "tsv": c.SCHEMA_FILE_EXPRESSION_TSV_ARRAY_FULL}
    return d[params["format"].lower()]

def schema_expression_search_no_filetype_mismatches(params):
    d = {"loom": c.SCHEMA_FILE_EXPRESSION_LOOM_ARRAY,
         "tsv": c.SCHEMA_FILE_EXPRESSION_TSV_ARRAY}
    return d[params["format"].lower()]

def schema_continuous_search_studyid(params, full=False):
     # render RNAGetContinuous template schema 
     output_filename = "temp.rnaget-continuous-studyid-" + params["studyID"] \
                       + ".json"
     template = c.SCHEMA_FILE_CONTINUOUS_STUDYID_TEMPLATE
     replace_l = [['["VAR_STUDYIDS"]', '["%s"]' % (params["studyID"])]]
     render_and_write_temp_schema(output_filename, template, replace_l)

     # render RNAGetContinuousArray template schema
     arr_output_filename = "temp.rnaget-continuous-array-studyid-" \
                           + params["studyID"] + ".json"
     arr_template = c.SCHEMA_FILE_CONTINUOUS_ARRAY_STUDYID_TEMPLATE
     arr_replace_l = [
          ["VAR_ARRAY_FILENAME", arr_output_filename],
          ["VAR_SINGLE_FILENAME", output_filename],
     ]
     if full:
          arr_replace_l.append(['"minItems": 0', '"minItems": 1'])

     render_and_write_temp_schema(arr_output_filename, arr_template, 
                                  arr_replace_l)
     
     return arr_output_filename


def schema_continuous_search_studyids_match(params):
     return schema_continuous_search_studyid(params, full=True)

def schema_continuous_search_no_studyid_mismatches(params):
     return schema_continuous_search_studyid(params)
