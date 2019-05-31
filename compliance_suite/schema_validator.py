# -*- coding: utf-8 -*-
"""Module compliance_suite.schema_validator.py

This module contains class definition for SchemaValidator, which compares a
JSON object instance against a known schema that it should match.
"""

from jsonschema import validate
from jsonschema import RefResolver
from jsonschema.exceptions import ValidationError
from compliance_suite.config.constants import *
import os
import json
import requests

class SchemaValidator(object):
    """Validates a JSON object instance against a known schema it should match.

    The SchemaValidator compares a JSON object against a schema using the 
    JSON Schema library/API. If the object matches its corresponding schema,
    then tests will pass and no error will be raised. If the object does not
    match its corresponding schema, the test will fail.

    Attributes:
        resolver (RefResolver): reference resolver that points references to
            other schema files to the correct directory
        schema_json (dict): dictionary representation of the JSON schema file 
    """

    def __init__(self, schema_file):
        """instantiates a SchemaValidator object

        Args:
            schema_file (string): name of JSON schema file (without directory)
        """

        # reference resolved to "schemas" directory in this library,
        # schema loaded
        schema_dir = os.path.abspath(SCHEMA_RELATIVE_DIR)
        self.resolver = RefResolver('file://' + schema_dir + "/", None)
        self.schema_json = json.loads(
            open(schema_dir + "/" + schema_file, "r").read()
        )
        
    def validate_instance(self, instance_json):
        """validate that a json object matches the schema

        Args:
            instance_json (dict): dictionary representation of json object

        Returns:
            validation_result (dict): contains info on whether instance passed
                or fail validation, and the exact error message produced by the
                validation
        """

        # test initialized as passing
        validation_result = {
            "status": 1,
            "exception_class": "",
            "message": ""
        }

        try:
            # api method to compare json instance to the schema
            validate(instance=instance_json, schema=self.schema_json,
                     resolver=self.resolver)

        except ValidationError as e:
            # if the api method raises an error, the result dictionary set
            # to include failure status and error message
            validation_result["status"] = -1
            validation_result["exception_class"] = str(e.__class__.__name__)
            validation_result["message"] = e.message

        return validation_result
