from jsonschema import validate
from jsonschema import RefResolver
from jsonschema.exceptions import ValidationError
from compliance_suite.constants import *
import os
import json
import requests

class SchemaValidator(object):

    def __init__(self, schema_file):
        schema_dir = os.path.abspath(SCHEMA_RELATIVE_DIR)
        self.resolver = RefResolver('file://' + schema_dir + "/", None)
        self.schema_json = json.loads(
            open(schema_dir + "/" + schema_file, "r").read()
        )
        
    def validate_instance(self, instance_json):
        validation_result = {
            "status": 1,
            "exception_class": "",
            "message": ""
        }

        try:
            validate(instance=instance_json, schema=self.schema_json,
                     resolver=self.resolver)

        except ValidationError as e:
            validation_result["status"] = -1
            validation_result["exception_class"] = str(e.__class__.__name__)
            validation_result["message"] = e.message

        return validation_result
