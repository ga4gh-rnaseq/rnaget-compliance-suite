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
study_ids_files = {}
expression_ids_files = {}
data_dir = "unittests/testdata/json_instances/"

@app.route("/projects/search")
def search_project():
    """search for projects based on filters in request
    
    Requests made to this route will return all projects on the local server
    that match request parameters/filters. If no parameters are provided, all
    projects will be returned as JSON

    Returns:
        response (str): JSON string of matched projects
    """

    matches = []
    possible_filters = ["version", "name"]

    for f in project_ids_files.values():
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

    return "[" + ",".join(matches) + "]"

@app.route("/projects/<project_id>")
def get_project(project_id):
    """get specific project for requested id

    Requests made to this route will return the project associated with the
    requested id if such a project exists. A 404 response will be returned if
    a project with requested id does not exist. If project id "NA" is submitted,
    a 501 response will be issued, simulating what would happen if the projects
    routes were not implemented.

    Args:
        project_id (str): project id
    
    Returns:
        response (str): JSON string of requested project
    """
    
    response = None
    if project_id in project_ids_files.keys():
        json_file = data_dir + project_ids_files[project_id]
        if os.path.exists(json_file):
            response = Response(open(json_file, "r").read(), status=200)
        else:
            response = Response(not_found_json, status=404)
    else:
        if project_id == "NA": # endpoint not implemented simultation,
                               # return 501 instead of 404
            response = Response(not_found_json, status=501)
        else:    
            response = Response(not_found_json, status=404)
    
    return response

@app.route("/studies/<study_id>")
def get_study(study_id):
    """get specific study for requested id

    Requests made to this route will return the study associated with the
    requested id if such a study exists. A 404 response will be returned if
    a study with requested id does not exist. If study id "NA" is submitted,
    a 501 response will be issued, simulating what would happen if the study
    routes were not implemented.

    Args:
        study_id (str): study id
    
    Returns:
        response (str): JSON string of requested study
    """

    response = None
    if study_id in study_ids_files.keys():
        json_file = data_dir + study_ids_files[study_id]
        if os.path.exists(json_file):
            response = Response(open(json_file, "r").read(), status=200)
        else:
            response = Response(not_found_json, status=404)
    else:
        if study_id == "NA": # endpoint not implemented simultation,
                               # return 501 instead of 404
            response = Response(not_found_json, status=501)
        else:    
            response = Response(not_found_json, status=404)
    
    return response

@app.route("/expressions/<expression_id>")
def get_expression(expression_id):
    """get specific expression for requested id

    Requests made to this route will return the expression associated with the
    requested id if such an expression exists. A 404 response will be returned
    if an expression with requested id does not exist. If expression id "NA" is
    submitted, a 501 response will be issued, simulating what would happen if
    the expressions routes were not implemented.

    Args:
        expression_id (str): expression id
    
    Returns:
        response (str): JSON string of requested expression
    """

    response = None
    if expression_id in expression_ids_files.keys():
        json_file = data_dir + expression_ids_files[expression_id]
        if os.path.exists(json_file):
            response = Response(open(json_file, "r").read(), status=200)
        else:
            response = Response(not_found_json, status=404)
    else:
        if expression_id == "NA": # endpoint not implemented simultation,
                               # return 501 instead of 404
            response = Response(not_found_json, status=501)
        else:    
            response = Response(not_found_json, status=404)
    
    return response