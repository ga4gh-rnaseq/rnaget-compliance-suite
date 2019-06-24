import compliance_suite.config.constants as c
import compliance_suite.schema_validator as sv
import os

def get_temp_filename(template_filename, value):
     return "temp." + template_filename.replace(".json", "") \
            + "-" + value + ".json"

def render_and_write_temp_schema(output_filename, template, replace_l):
     schema_dir = os.path.dirname(sv.__file__) \
                     + "/" + c.SCHEMA_RELATIVE_DIR
     template_file = schema_dir + "/" + template
     json = open(template_file, "r").read()
     for replace in replace_l:
          json = json.replace(replace[0], replace[1])
     out_path = schema_dir + "/" + output_filename
     open(out_path, "w").write(json)

def render_endpoint_object_and_array(obj_filename, obj_template, obj_replace_l,
     arr_filename, arr_template, arr_replace_l, value, full=False):
     
     render_and_write_temp_schema(obj_filename, obj_template, obj_replace_l)
     if full:
          arr_replace_l.append(['"minItems": 0', '"minItems": 1'])
     render_and_write_temp_schema(arr_filename, arr_template, 
                                  arr_replace_l)

def schema_expression_search_format(params, full=False):
     value = params["format"]
     obj_template = c.SCHEMA_FILE_EXPRESSION_FORMAT_TEMPLATE
     obj_filename = get_temp_filename(obj_template, value)
     obj_replace_l = [
          ['["VAR_FORMATS"]', 
          '["%s", "%s"]' % (params["format"].lower(),
                            params["format"].upper())],
          ["VAR_FILENAME", obj_filename]
     ]
     
     arr_template = c.SCHEMA_FILE_EXPRESSION_ARRAY_FORMAT_TEMPLATE
     arr_filename = get_temp_filename(arr_template, value)
     arr_replace_l = [
          ["VAR_ARRAY_FILENAME", arr_filename],
          ["VAR_SINGLE_FILENAME", obj_filename]
     ]
     
     render_endpoint_object_and_array(obj_filename, obj_template,
          obj_replace_l, arr_filename, arr_template, arr_replace_l, 
          value, full)

     return arr_filename

def schema_expression_search_filetypes_match(params):
    return schema_expression_search_format(params, full=True)

def schema_expression_search_no_filetype_mismatches(params):
    return schema_expression_search_format(params)

def schema_continuous_search_studyid(params, full=False):
     value = params["studyID"]
     obj_template = c.SCHEMA_FILE_CONTINUOUS_STUDYID_TEMPLATE
     obj_filename = get_temp_filename(obj_template, value)
     obj_replace_l = [
          ['["VAR_STUDYIDS"]', '["%s"]' % (params["studyID"])],
          ['VAR_FILENAME', obj_filename]
     ]
     
     arr_template = c.SCHEMA_FILE_CONTINUOUS_ARRAY_STUDYID_TEMPLATE
     arr_filename = get_temp_filename(arr_template, value)
     arr_replace_l = [
          ["VAR_ARRAY_FILENAME", arr_filename],
          ["VAR_SINGLE_FILENAME", obj_filename]
     ]
     
     render_endpoint_object_and_array(obj_filename, obj_template,
          obj_replace_l, arr_filename, arr_template, arr_replace_l, 
          value, full)

     return arr_filename

def schema_continuous_search_studyids_match(params):
     return schema_continuous_search_studyid(params, full=True)

def schema_continuous_search_no_studyid_mismatches(params):
     return schema_continuous_search_studyid(params)
