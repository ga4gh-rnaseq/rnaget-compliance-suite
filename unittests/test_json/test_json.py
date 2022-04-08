import json

import compliance_suite.cli as cli
import compliance_suite.exceptions.test_status_exception as tse
from compliance_suite.user_config_parser import UserConfigParser


def validate_json(expected, actual):

    if type(expected) != type(actual):
        raise tse.JsonParseException("JSON type expected")

    if len(expected) != len(actual):
        raise tse.JsonParseException("JSON Key missing")

    for json_key in expected:

        if json_key != "phases":
            if json_key != "phases" and expected[json_key] != actual[json_key]:
                raise tse.JsonParseException("expected " + expected[json_key])

        expected_phases = expected["phases"]
        actual_phases = actual["phases"]

        for phase in range(len(expected["phases"])):
            if len(expected_phases[phase]) != len(actual_phases[phase]):
                raise tse.JsonParseException("Phases Key missing")

            for phase_key in expected_phases[phase]:

                if phase_key != "tests":
                    if expected_phases[phase][phase_key] != actual_phases[phase][phase_key]:
                        raise tse.JsonParseException("expected " + expected_phases[phase][phase_key])

                expected_tests = expected_phases[phase]["tests"]
                actual_tests = actual_phases[phase]["tests"]

                for test in range(len(expected_tests)):
                    if len(expected_tests[test]) != len(actual_tests[test]):
                        raise tse.JsonParseException("Tests Key missing") 

                    for test_key in expected_tests[test]:

                        if test_key != "cases":
                            if expected_tests[test][test_key] != actual_tests[test][test_key]:
                                raise tse.JsonParseException("expected " + expected_tests[test][test_key])

                        expected_cases = expected_tests[test]["cases"]
                        actual_cases = actual_tests[test]["cases"]

                        for case in range(len(expected_cases)):
                            if len(expected_cases[case]) != len(actual_cases[case]):
                                raise tse.JsonParseException("Cases Key missing")

                            for case_key in expected_cases[case]:
                                if expected_cases[case][case_key] != actual_cases[case][case_key]:
                                    raise tse.JsonParseException("expected " + expected_cases[case][case_key])

    print("Testing passed!")

def test_validate_json():
    user_config = "unittests/data/user_config/test_json.yaml"
    user_config = UserConfigParser(user_config)
    user_config.parse_config_file()
    user_config.validate_config_file()

    f = open("unittests/test_json/expected.json", "r")
    expected_json = json.load(f)

    actual = cli.test_report(user_config)

    actual.set_start_time("2222-22-22T22:22:22Z")
    actual.set_end_time("2222-22-22T22:22:22Z")

    for phase in actual.get_phases():
        phase.set_start_time("2222-22-22T22:22:22Z")
        phase.set_end_time("2222-22-22T22:22:22Z")

        for test in phase.get_tests():
            test.set_start_time("2222-22-22T22:22:22Z")
            test.set_end_time("2222-22-22T22:22:22Z")

            for case in test.get_cases():
                case.set_start_time("2222-22-22T22:22:22Z")
                case.set_end_time("2222-22-22T22:22:22Z")

    actual_json = json.loads(actual.to_json())

    validate_json(expected_json, actual_json)