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
from flask import Flask, Response, request

app = Flask(__name__, root_path='testdata')

not_found_json = '{"Message": "resource not found"}'
project_ids_files = {
    "43378a5d48364f9d8cf3c3d5104df560": "project_valid_0.json",
    "38n54mgtogq4nq2s5nfqcoop4160vso7": "project_invalid_0.json"
}
study_ids_files = {
    "6cccbbd76b9c4837bd7342dd616d0fec": "study_valid_0.json"
}
expression_ids_files = {
    "2a7ab5533ef941eaa59edbfe887b58c4": "expression_valid_0.json"
}
obj_type_d = {"projects": project_ids_files,
              "studies": study_ids_files,
              "expressions": expression_ids_files
}
filters_d = {"projects": ["version", "name"],
             "studies": ["version", "name"],
             "expressions": ["studyID"]}
data_dir = "unittests/testdata/json_instances/"

def get_response(body, status=200):
    return Response(body, status=status, mimetype="application/json")

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
        if obj_type not in obj_type_d.keys():
            raise Exception("Invalid object type specified")

        files_d = obj_type_d[obj_type]

        if obj_id in files_d.keys():
            json_file = data_dir + files_d[obj_id]
            if os.path.exists(json_file):
                response = get_response(open(json_file, "r").read())
            else:
                response = get_response(not_found_json, status=404)
        else:
            if obj_id == "NA": # endpoint not implemented simultation,
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
        if obj_type not in obj_type_d.keys():
            raise Exception("Invalid object type specified")

        possible_filters = filters_d[obj_type]
        
        for f in obj_type_d[obj_type].values():
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
        response_body = '''{"message": "invalid resource '%s'"}''' % obj_type
        response = get_response(response_body, status=400)

    return response

@app.route("/emptyresponse")
def emptyresponse():
    """Returns an empty response body so it can raise JSON parse exception"""
    return get_response("")


