# -*- coding: utf-8 -*-
"""Module unittests.test_schema_validator.py

This module contains methods to test the schema_validator module via pytest.
"""

import json
from compliance_suite.schema_validator import SchemaValidator
import compliance_suite.config.constants as c

json_dir = "unittests/data/json_instances/"
project_valid = json_dir + "project_valid.json"
study_valid = json_dir + "study_valid.json"

def json_file_to_dict(file_path):
    """load a dict from file containing JSON

    Args:
        file_path (str): path to JSON file
    
    Returns:
        json_dict (dict): object representation of JSON contained in file
    """

    return json.loads(open(file_path, "r").read())

def template(messages_list, filename_template, schema, outcome):
    """generic template for asserting correct/incorrect JSON instances

    This method acts as a template for all subsequent schema validation unit
    tests. It asserts that the correct error messages are generated for a
    schema mismatch, and also that the test result has the correct status code
    (1 for pass, -1 for fail)

    Args:
        messages_list (list): each element represents what error message SHOULD
            be generated for the type of schema mismatch
        filename_template (str): filename pattern common to all the json files
            that will be tested against
        schema (str): file that contains the correct JSON schema to be used for
            all tests in the set
        outcome (int): 1 for expected passes, -1 for expected fails
    """

    # for each case, assert that the result status matches the expected fail
    # or pass integer, and also assert that the expected message matches the
    # actual message
    for i in range(0, len(messages_list)):
        json_file = json_dir + filename_template + "_" + str(i) + ".json"
        sv = SchemaValidator(schema)
        result = sv.validate_instance(json_file_to_dict(json_file))
        assert result["status"] == outcome
        assert result["message"] == messages_list[i]
        sv.delete_temp()

def schema_pass_template(count, filename_template, schema):
    """template for tests that are expected to pass schema validation"""

    messages_list = ["" for i in range(0, count)]
    template(messages_list, filename_template, schema, 1)

def schema_fail_template(messages_list, filename_template, schema):
    """template for tests that are expected to fail schema validation"""

    template(messages_list, filename_template, schema, -1)

def test_project_valid():
    """asserts a valid project instance passes schema validation"""

    schema_pass_template(1, "project_valid", c.SCHEMA_FILE_PROJECT)

def test_project_invalid():
    """asserts invalid project instances fail validation with correct message"""

    m = [
        "'id' is a required property",
        "1 is not of type 'string'",
        "2 is not of type 'string'"
    ]
    schema_fail_template(m, "project_invalid", c.SCHEMA_FILE_PROJECT)

def test_study_valid():
    """asserts valid study instance passes schema validation"""

    schema_pass_template(1, "study_valid", c.SCHEMA_FILE_STUDY)

def test_study_invalid():
    """asserts invalid study instances fail validation with correct message"""

    m = [
        "'id' is a required property",
        "1 is not of type 'string'"
    ]
    schema_fail_template(m, "study_invalid", c.SCHEMA_FILE_STUDY)

def test_expression_valid():
    """asserts valid expression instance passes schema validation"""

    schema_pass_template(0, "expression_valid", c.SCHEMA_FILE_EXPRESSION)

def test_expression_invalid():
    """asserts invalid expression instances fail with correct message"""

    m = [
        "'url' is a required property",
        "'units' is a required property",
        "1 is not of type 'string'"
    ]
    schema_fail_template(m, "expression_invalid", c.SCHEMA_FILE_EXPRESSION)