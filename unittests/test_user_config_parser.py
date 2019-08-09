# -*- coding: utf-8 -*-
"""Module unittests.test_user_config_parser.py

This module contains methods to test the user_config_parser module via pytest.
"""

from compliance_suite.user_config_parser import UserConfigParser

yaml_dir = "unittests/data/user_config/"
user_config_pass = "config_template.yaml"
user_config_file_not_found = "file_not_found.yaml"

def test_constructor():
    """asserts attributes set correctly via constructor"""

    parser = UserConfigParser(user_config_pass)
    assert parser.config_file == user_config_pass
    assert parser.d == None

def test_parse_config_file_pass():
    """asserts yaml successfully loaded and contains expected values"""

    parser = UserConfigParser(user_config_pass)
    parser.parse_config_file()
    assert parser.d != None
    assert len(parser.d["servers"]) == 2

    server_a = parser.d["servers"][0]
    assert server_a["server_name"] == "Caltech"
    assert server_a["base_url"] == "https://felcat.caltech.edu/rnaget/"

def test_parse_config_file_not_found():
    """asserts correct error raised when yaml file not found"""

    parser = None
    try:
        parser = UserConfigParser(user_config_file_not_found)
        parser.parse_config_file()
    except FileNotFoundError as e:
        assert str(e) == "user config file: " + user_config_file_not_found \
                         + " not found"

def test_validate_config_file_pass():
    """asserts correct yaml file passes validation"""

    parser = UserConfigParser(user_config_pass)
    parser.parse_config_file()
    parser.validate_config_file()

def test_validate_config_file_failures():
    """asserts parser invalidates different yaml files with message"""

    messages = [
        '"servers" should be the only root key',
        '"servers" should be the only root key',
        "YAML config file could not be parsed. Please refer to the template "
            + "config file.",
        'value of implemented:expressions must be a boolean',
        'wrongendpoint not a valid endpoint',
        "missing attribute(s) from server 1: server_name"
    ]

    for i in range(0,6):
        config_file = yaml_dir + "fail_" + str(i) + ".yaml"
        message = messages[i]

        try:
            parser = UserConfigParser(config_file)
            parser.parse_config_file()
            parser.validate_config_file()
            assert True == False # config parser must raise an error before
                                 # getting to this line
        except Exception as e:
            assert message == str(e)

