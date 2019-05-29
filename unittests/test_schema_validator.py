import json

from compliance_suite.schema_validator import SchemaValidator
import compliance_suite.config.constants as c

json_dir = "unittests/testdata/json_instances/"

project_valid = json_dir + "project_valid.json"
study_valid = json_dir + "study_valid.json"

def json_file_to_dict(file_path):
    return json.loads(open(file_path, "r").read())

def template(messages_list, filename_template, schema, outcome):
    for i in range(0, len(messages_list)):
        json_file = json_dir + filename_template + "_" + str(i) + ".json"
        sv = SchemaValidator(schema)
        result = sv.validate_instance(json_file_to_dict(json_file))
        assert result["status"] == outcome
        assert result["message"] == messages_list[i]

def schema_pass_template(count, filename_template, schema):
    messages_list = ["" for i in range(0, count)]
    template(messages_list, filename_template, schema, 1)

def schema_fail_template(messages_list, filename_template, schema):
    template(messages_list, filename_template, schema, -1)

def test_project_valid():
    schema_pass_template(1, "project_valid", c.SCHEMA_FILE_PROJECT)

def test_project_invalid():
    m = [
        "'id' is a required property",
        "Additional properties are not allowed ('additionalAttribute' was " +
            "unexpected)",
        "1 is not of type 'string'",
        "2 is not of type 'string'"
    ]
    schema_fail_template(m, "project_invalid", c.SCHEMA_FILE_PROJECT)

def test_study_valid():
    schema_pass_template(1, "study_valid", c.SCHEMA_FILE_STUDY)

def test_study_invalid():
    m = [
        "'id' is a required property",
        "Additional properties are not allowed ('additionalAttribute' was " +
            "unexpected)",
        "1 is not of type 'string'"
    ]
    schema_fail_template(m, "study_invalid", c.SCHEMA_FILE_STUDY)

def test_expression_valid():
    schema_pass_template(1, "expression_valid", c.SCHEMA_FILE_EXPRESSION)

def test_expression_invalid():
    m = [
        "'id' is a required property",
        "'units' is a required property",
        "Additional properties are not allowed ('additionalAttribute' was " +
            "unexpected)",
        "1 is not of type 'string'"
    ]
    schema_fail_template(m, "expression_invalid", c.SCHEMA_FILE_EXPRESSION)

