# -*- coding: utf-8 -*-
"""Module unittests.unittests_server.py

This module contains a Flask app, to be run locally during unit testing. The app
serves requests issued during unit testing, responding with projects, studies,
expressions, etc.

Attributes:
    app (Flask): flask app/local server
    not_found_json (str): response when requested resource not found
    project_ids_files (dict): id and associated file for requested projects
    study_ids_files (dict): id and associated file for requested studies
    expression_ids_files (dict): id, associated file for requested expressions
    data_dir (str): path to dir containing json instance files
"""

import os
import json
from flask import Flask, Response, request, send_file

app = Flask(__name__, root_path='unittests/data/matrices')

not_found_json = '{"Message": "resource not found"}'

file_dict = {
    "projects": {
        "valid": {
            "9c0eba51095d3939437e220db196e27b": "project_valid_0.json",
        }, "invalid": {
            "b6b3431e95f6cc6dbc69b0f0bbcb73a3": "project_invalid_mismatchedid.json",
            "251de42306846bffec4290dca8064cb0": "project_invalid_notjson.txt"
        }
    },
    "studies": {
        "valid": {
            "f3ba0b59bed0fa2f1030e7cb508324d1": "study_valid_0.json"
        }, "invalid": {
        }
    },
    "expressions": {
        "valid": {
            "ac3e9279efd02f1c98de4ed3d335b98e": "expression_valid_0.json"
        }, "invalid": {
        }
    },
    "continuous": {
        "valid": {
            "5e22e009f41fc53cbea094a41de8798f": "continuous_placeholder.json"
        }, "invalid": {
        }
    }
}

# get the correct continuous loom file based on the parameters supplied to 
# request
continuous_file_by_params = {
    "": "continuous/continuous.loom",
    "chr=chr1,start=30,end=50": "continuous/continuous_1.loom"
}

filters_d = {"projects": ["version", "name"],
             "studies": ["version", "name"],
             "expressions": ["studyID"]}
data_dir = "unittests/data/json_instances/"

def get_response(body, status=200, mimetype="application/json"):
    return Response(body, status=status, mimetype=mimetype)

@app.route("/<obj_type>/<obj_id>")
def get_project(obj_type, obj_id):
    """get specific object of specific type with requested id

    Requests made to this route will return the object (project, study, 
    expression) associated with the requested id if such an object exists. A 404
    response will be returned if an object with requested id does not exist. If
    object id "NA" is submitted, a 501 response will be issued, simulating what
    would happen if the route was not implemented.

    Args:
        obj_type (str): object type: project, study, or expression
        obj_id (str): the object's id
    
    Returns:
        response (str): JSON string of requested object
    """
    
    response = None

    try:
        if obj_type not in file_dict.keys():
            raise Exception("Invalid object type specified")

        files_d = {}
        files_d.update(file_dict[obj_type]["valid"])
        files_d.update(file_dict[obj_type]["invalid"])

        if obj_id in files_d.keys():
            json_file = data_dir + files_d[obj_id]
            if os.path.exists(json_file):
                if obj_type == "continuous":

                    potential_params = ["chr", "start", "end"]
                    used_params = []
                    for potential_param in potential_params:
                        param_val = request.args.get(potential_param)
                        if param_val:
                            used_params.append("%s=%s" % (str(potential_param), 
                                                         str(param_val)))
                    
                    param_key = ",".join(used_params)
                    print(param_key)
                    path = continuous_file_by_params[param_key]
                    print(path)
                    response = send_file(path, mimetype="application/vnd.loom")
                else:
                    response = get_response(open(json_file, "r").read())
            else:
                response = get_response(not_found_json, status=404)
        else:
            if obj_id == "NA": # endpoint not implemented simulation,
                                # return 501 instead of 404
                response = get_response(not_found_json, status=501)
            else:    
                response = get_response(not_found_json, status=404)

    except Exception as e:
        response_body = '''{"message": "invalid resource '%s'"}''' % obj_type
        response = get_response(response_body, status=400)
    
    return response

@app.route("/<obj_type>/search")
def search_for_object(obj_type):
    """search for requested object type based on filters in request
    
    Requests made to this route will return all requested objects of the 
    specified type (project, study, expression) on the local server that match
    request parameters/filters. If no parameters are provided, all objects
    will be returned as JSON

    Returns:
        response (str): JSON string of matched objects
    """

    matches = []
    response = None

    try:
        if obj_type not in file_dict.keys():
            raise Exception("Invalid object type specified")

        possible_filters = filters_d[obj_type]
        
        for f in file_dict[obj_type]["valid"].values():
            json_file = data_dir + f
            json_s = open(json_file, "r").read()
            json_obj = json.loads(json_s)
            add_to_matches = True

            for filter_name in possible_filters:
                filter_val = request.args.get(filter_name)
                if filter_val:
                    if json_obj[filter_name] != filter_val:
                        add_to_matches = False
            
            if add_to_matches:
                matches.append(json_s)

        response_body = "[" + ",".join(matches) + "]"
        response = get_response(response_body, status=200)

    except Exception as e:
        print("bad request")
        response_body = '''{"message": "invalid resource '%s'"}''' % obj_type
        response = get_response(response_body, status=400)

    return response

@app.route("/emptyresponse")
def emptyresponse():
    """Returns an empty response body so it can raise JSON parse exception"""
    return get_response("")

@app.route("/matrices/<obj_type>/<filename>")
def get_matrix(obj_type, filename):
    path = "%s/%s" % (obj_type, filename)
    return send_file(path, mimetype="application/vnd.loom")
