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
from click.testing import CliRunner
from multiprocessing import Process

user_config_dir = "unittests/testdata/user_config/"
user_config_success = user_config_dir + "config_0.yaml"
user_config_failure = user_config_dir + "fail_0.yaml"
json_output_file = "unittest_output.json"

def remove_web_archive():
    """remove web archives produced by unittests"""

    os.system("rm web_*")

def test_main():
    """asserts that the 'main' method of cli module can be executed"""

    runner = CliRunner()
    runner.invoke(main)
    assert True

def test_report():
    """asserts that the 'report' method of cli module executes successfully"""

    runner = CliRunner()
    result = runner.invoke(report, ['-c', user_config_success])
    assert result.exit_code == 0

def test_exceptions():
    """asserts program raises appropriate exceptions with incorrect params"""

    # empty cli, exception should be caught but no error raised
    runner = CliRunner()
    result = runner.invoke(report, [])
    assert result.exit_code == 0

    # incorrectly formatted user config submitted, exception should be caught
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_failure])

    # non-existing user config submitted, exception should be caught
    runner = CliRunner()
    result = runner.invoke(report, ["-c", "file.yaml"])
    assert result.exit_code == 0

    # server uptime is a string, not number, exception should be caught
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_failure, 
                                    "--uptime", 'String'])
    assert result.exit_code == 0

    remove_web_archive()

def test_json_path():
    """asserts correct execution when json path provided"""

    # json output set to file, asserts prog runs to completion
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_success, "--json",
                                    json_output_file])
    os.system("rm " + json_output_file)
    assert result.exit_code == 0
    
    # json output set to stdout, asserts prog runs to completion
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_success, "--json",
                                    "-"])
    assert result.exit_code == 0

    remove_web_archive()

def test_mock_server():
    """asserts mock server is launched and shutdown without error"""
    
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_success, "--serve",
                                    "--uptime", '1'])
    assert result.exit_code == 0

    remove_web_archive()
