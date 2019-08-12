# -*- coding: utf-8 -*-
"""Module unittests.test_cli.py

This module contains methods to test the cli module via pytest.

Attributes:
    user_config_dir (str): path to directory containing sample user configs
    user_config_success (str): file containing correct user config
    user_config_failure (str): file containing error-generating config
    json_output_file (str): path to output file
"""

import os
import click
import signal
from compliance_suite.cli import main, report
from unittests.constants import OUTPUT_DIR as od
from unittests.methods import *
from click.testing import CliRunner
from multiprocessing import Process

user_config_dir = "unittests/data/user_config/"
user_config_success = user_config_dir + "config_0.yaml"
user_config_failure = user_config_dir + "fail_0.yaml"
json_output_file = "unittest_output.json"

def test_main():
    """asserts that the 'main' method of cli module can be executed"""

    runner = CliRunner()
    runner.invoke(main)
    assert True

def test_report():
    """asserts that the 'report' method of cli module executes successfully"""

    remove_output_dirs()
    runner = CliRunner()
    result = runner.invoke(report, ['-c', user_config_success])
    assert result.exit_code == 0
    remove_output_dirs()

    os.mkdir(od)
    runner = CliRunner()
    result = runner.invoke(report, ['-c', user_config_success, 
                                    '-o', od, '--no-tar', '-f'])
    assert result.exit_code == 0
    remove_output_dirs()

    # runner = CliRunner()
    # result = runner.invoke(report, ['-c', user_config_success, '-o', od, 
    #                                 '--no-tar', '-f', '--serve', '-u', '2'])
    # assert result.exit_code == 0

def test_exceptions():
    """asserts program raises appropriate exceptions with incorrect params"""

    remove_output_dirs()
    # empty cli, exception should be caught, program exits with status code "1"
    runner = CliRunner()
    result = runner.invoke(report, [])
    assert result.exit_code == 1
    remove_output_dirs()

    # incorrectly formatted user config submitted, exception should be caught
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_failure, "-o", od])
    assert result.exit_code == 1
    remove_output_dirs()

    # non-existing user config submitted, exception should be caught,
    # program exits with status code "1"
    runner = CliRunner()
    result = runner.invoke(report, ["-c", "file.yaml", "-o", od])
    assert result.exit_code == 1
    remove_output_dirs()

    # server uptime is a string, not number, exception should be caught,
    # program exits with status code "1"
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_failure, "-o", od,
                                    "--uptime", 'String'])
    assert result.exit_code == 1
    remove_output_dirs()

    # output directory does not exist
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_success, "-o", 
                           "directory/doesnot/exist"])
    assert result.exit_code == 1
    remove_output_dirs()

    # cannot overwrite output directory
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_success, "-o", 
                           "unittests/data/results"])
    assert result.exit_code == 1
    remove_output_dirs()


# TODO: re-enable test once I've figured out how to get it working on travis ci
# def test_mock_server():
#     """asserts mock server is launched and shutdown without error"""
#     
#     remove_output_dir()
#     runner = CliRunner()
#     result = runner.invoke(report, ["-c", user_config_success, "-o", od, 
#                                     "--serve", "--uptime", '1'])
#     assert result.exit_code == 0
