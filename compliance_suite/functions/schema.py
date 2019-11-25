# -*- coding: utf-8 -*-
"""Module compliance_suite.functions.schema.py

Functions to create dynamic JSON schemas according to test case. Each function
in this module should write a temporary JSON schema file that is used in the 
validation section of API testing and return its filename
"""

import compliance_suite.config.constants as c
import compliance_suite.schema_validator as sv
import json
import os

def render_and_write_temp_schema(output_filename, template, replace_l):
     """Write a temporary schema file
     
     Renders a temporary schema file from a template. Each element in the 
     replacement list indicates a string to replace in the template file, as
     well as what to replace it with

     Arguments:
         output_filename (str): output file path
         template (str): JSON schema template filename
         replace_l (list): replacement list
     """

     # open the template schema
     schema_dir = os.path.dirname(sv.__file__) \
                     + "/" + c.SCHEMA_RELATIVE_DIR
     template_file = schema_dir + "/" + template
     json = open(template_file, "r").read()

     # for each item in the replacement list, replace the placeholder text
     # in the template, with the true value to be output to the temporary
     # schema
     for replace in replace_l:
          json = json.replace(replace[0], replace[1])

     # write the temporary schema file
     out_path = schema_dir + "/" + output_filename
     open(out_path, "w").write(json)

def render_endpoint_object_and_array(obj_filename, obj_template, obj_replace_l,
     arr_filename, arr_template, arr_replace_l, value, full=False):
     """Render a temporary schema object, and an array full of temp objects

     Arguments:
         obj_filename (str): filename for object
         obj_template (str): JSON schema template file for object
         obj_replace_l (list): replacement list for object
         arr_filename (str): filename for array
         arr_template (str): JSON schema template file for array
         arr_replace_l (list): replacement list for array
         value (str): value to differentiate temp file
         full (bool): if full, set minItems to 1 for the array schema
     """
     
     # render the object schema
     render_and_write_temp_schema(obj_filename, obj_template, obj_replace_l)

     if full:
          arr_replace_l.append(['"minItems": 0', '"minItems": 1'])

     # render the array schema
     render_and_write_temp_schema(arr_filename, arr_template, arr_replace_l)

def schema_require_matching_id(runner, node, params):
    """Generate schema that requires request id to match response id

    Arguments:
        runner (Runner): reference to Runner object
        node (Node): reference to Node object
        params (dict): test case parameters
    
    Returns:
        (str): file path for temporary schema
    """

    template = "rnaget-reqid-template.json"
    schemas_by_obj_type = {
        "projects": "rnaget-project.json",
        "studies": "rnaget-study.json",
        "expressions": "rnaget-expression.json",
        "continuous": "rnaget-continuous.json"
    }

    obj_type = node.kwargs["obj_type"]
    obj_id = node.kwargs["obj_instance"]["id"]
    output_filename = "temp." + obj_type + "." + obj_id + ".reqid.json"

    replace_l = [
        ["VAR_FILENAME", output_filename],
        ["VAR_REF", schemas_by_obj_type[obj_type]],
        ["VAR_ID", obj_id]
    ]
    render_and_write_temp_schema(output_filename, template, replace_l)
    return output_filename

def schema_require_matching_search_params(runner, node, params, full=True):
    """Generate schema requiring matching search params and response params

    Arguments:
        runner (Runner): reference to Runner object
        node (Node): reference to Node object
        params (dict): test case parameters
        full (bool): if true, create array schema requiring at least 1 element
    
    Returns:
        (str): file path for temporary schema
    """

    schemas_by_obj_type = {
        "projects": "rnaget-project.json",
        "studies": "rnaget-study.json",
        "expressions": "rnaget-ticket.json",
        "continuous": "rnaget-ticket.json"
    }
    array_or_single_by_obj_type = {
        "projects": "array",
        "studies": "array",
        "expressions": "single",
        "continuous": "single"
    }

    obj_type = node.kwargs["obj_type"]
    obj_id = node.kwargs["obj_instance"]["id"]

    obj_template = "rnaget-reqsearchparams-template.json"
    arr_template = "rnaget-reqsearchparams-array-template.json"
    obj_filename = "temp." + obj_type + "." + obj_id + ".reqsearchparams.json"
    arr_filename = "temp." + obj_type + "." + obj_id + \
        ".reqsearchparams.array.json"

    # format search parameters as JSON schema that can be subbed into the file
    params_json_schema = []
    for param_key in params.keys():
        if param_key != "tags":
            property_key = "fileType" if param_key == "format" else param_key
            properties = {
                "type": "string",
                "enum": [params[param_key]]
            }

            params_json_schema.append('"%s": %s' % (
                property_key, json.dumps(properties)))

    obj_replace_l = [
        ["VAR_FILENAME", obj_filename],
        ["VAR_REF", schemas_by_obj_type[obj_type]],
        ['"VAR_SEARCH_PARAMS": {}', ",".join(params_json_schema)]
    ]
    arr_replace_l = [
        ["VAR_ARRAY_FILENAME", arr_filename],
        ["VAR_SINGLE_FILENAME", obj_filename]
    ]
    value = "1"

    render_endpoint_object_and_array(obj_filename, obj_template, obj_replace_l,
        arr_filename, arr_template, arr_replace_l, value, full=full)

    ret = arr_filename
    if array_or_single_by_obj_type[obj_type] == "single":
        ret = obj_filename
    
    return ret

def schema_require_matching_search_params_allow_empty(runner, node, params):
    """Generate schema requiring matching params, allow empty arrays

    Arguments:
        runner (Runner): reference to Runner object
        node (Node): reference to Node object
        params (dict): test case parameters
    
    Returns:
        (str): file path for temporary schema
    """

    return schema_require_matching_search_params(runner, node, params,
        full=False)
