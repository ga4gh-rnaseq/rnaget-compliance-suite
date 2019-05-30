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
    os.system("rm web_*")

def test_main():
    runner = CliRunner()
    runner.invoke(main)
    assert True

def test_report():
    runner = CliRunner()
    result = runner.invoke(report, ['-c', user_config_success])
    assert result.exit_code == 0

def test_exceptions():
    runner = CliRunner()
    result = runner.invoke(report, [])
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_failure])

    runner = CliRunner()
    result = runner.invoke(report, ["-c", "file.yaml"])
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_failure, 
                                    "--uptime", 'String'])
    assert result.exit_code == 0

    remove_web_archive()

def test_json_path():
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_success, "--json",
                                    json_output_file])
    os.system("rm " + json_output_file)
    assert result.exit_code == 0
    

    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_success, "--json",
                                    "-"])
    assert result.exit_code == 0

    remove_web_archive()

def test_mock_server():
    runner = CliRunner()
    result = runner.invoke(report, ["-c", user_config_success, "--serve",
                                    "--uptime", '1'])
    assert result.exit_code == 0

    remove_web_archive()
