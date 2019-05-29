# -*- coding: utf-8 -*-
"""Module compliance_suite.cli.py

This module contains the report generation entry point and associated methods
for the RNAGet compliance testing suite. Command line arguments are parsed
and validated before the TestRunner tests are initiated. JSON report is written
to file and a local server serving the report can be spun up if user specifies.
"""

import time
import json
import os
import sys
import tarfile

import click

from compliance_suite.report_server import ReportServer
from compliance_suite.test_runner import TestRunner
from compliance_suite.user_config_parser import UserConfigParser
from compliance_suite.exceptions.argument_exception import ArgumentException
from compliance_suite.exceptions.user_config_exception import \
    UserConfigException
from compliance_suite.config.tests import TESTS_BY_OBJECT_TYPE

def scan_for_errors(json):
    """generate high-level summaries from available results data structure
    
    This routine loops through the available results data structure and
    generates high-level summaries for the main test routines.
    High-level summaries for:
        - project
        - study
        - expression

    Args:
        json (dict): dictionary structure of test results JSON report
    """

    high_level_summary = {}
    available_tests = ('project_get')

    for server in json:
        for obj_type in ["projects", "studies", "expressions"]:
            for obj_id in server["test_results"][obj_type].keys():
                server_tests = server["test_results"][obj_type][obj_id]
                
                for high_level_name in (available_tests):
                    # We are successful unless proven otherwise
                    result = 1
                    for test in server_tests:
                        if high_level_name in test["parents"]:
                            """
                            if test['warning']:
                                result = test["result"]
                                break
                            """
                    high_level_summary[high_level_name] = {
                        'result': result,
                        'name': high_level_name
                    }

                server["high_level_summary"] = high_level_summary
    
@click.group()
def main():
    """Main method. Deprecated as program entry is through 'report' method"""

@main.command(help='run compliance utility report using base urls')
@click.option('--user-config', '-c', help="path to user config yaml file")
@click.option('--file_path_name', '-fpn', default='web', 
              help='to create a tar.gz file')
@click.option('--json_path', '--json',  
              help='create a json file report. Setting this to "-" will emit '
              + 'to standard out')
@click.option('--serve', is_flag=True, help='spin up a server')
@click.option('--uptime', '-u', default='3600',
              help='time that server will remain up in seconds')
@click.option('--no-web', is_flag=True, help='skip the creation of a tarball')
def report(user_config, file_path_name, json_path, serve, uptime, no_web):
    """Program entrypoint. Executes compliance tests and generates report

    This method parses the CLI command 'report' to execute the report session
    and generate report on terminal, html file and json file if provided by the
    user

    Arguments:
        user_config (str): Required. Path to user config YAML file
        file_path_name (str): Optional. File name for w:gz file of web folder.
            Default is web_<int>.tar.gz
        json_path (str): Optional. Path to dump the final JSON content to
        serve (bool): Optional. If true, spin up a server
        no_web (bool): Optional. If true, do not dump a webfile
    """

    final_json = []

    try:

        # check that the user config has been specified, if not, program
        # cannot proceed with tests
        if not user_config:
            raise ArgumentException(
                'No user config file provided. Specify path to yaml file with '
                + '-c'
            )
        
        # check that the server uptime is a valid integer
        if not uptime.isdigit():
            raise ArgumentException('Server uptime is not a valid integer.')

        # parse the user config and check it for any errors, raising errors
        # as necessary
        user_config = UserConfigParser(user_config)
        user_config.parse_config_file()
        user_config.validate_config_file()
        
        # for each server in the user config, create a TestRunner
        # run associated tests and add the resulting JSON to the final json
        # report
        for server_config in user_config.d["servers"]:
            tr = TestRunner(server_config)

            token = None
            if "token" in server_config.keys():
                token = server_config["token"]

            if token:
                tr.headers['Authorization'] = 'Bearer ' + str(token)
            tr.run_tests()
            final_json.append(tr.generate_final_json())

        scan_for_errors(final_json)

        # write final report to output file if specified
        if json_path is not None:
            if json_path == '-':
                json.dump(final_json, sys.stdout)
            else:
                with open(json_path, 'w') as outfile:
                    json.dump(final_json, outfile)

        WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')

        # write tar.gz archive of report and web files if user specified
        if not no_web:
            if file_path_name is not None:
                with open(os.path.join(WEB_DIR,
                          'temp_result.json'), 'w+') as outfile:
                    json.dump(final_json, outfile)

                index = 0
                while(os.path.exists(file_path_name + '_' + str(index) 
                                     + '.tar.gz')):
                    index = index + 1
                with tarfile.open(
                    file_path_name + '_' + str(index) + '.tar.gz', "w:gz"
                ) as tar:
                    tar.add(WEB_DIR, arcname=os.path.basename(WEB_DIR))

        # start server if user specified --serve
        if serve is True:
            server = ReportServer()
            server.set_free_port()
            server.serve_thread(uptime=int(uptime))
            
    # handle various exception classes, each time printing the usage
    # instructions to terminal along with a description of what went wrong
    except ArgumentException as e:
        with click.Context(report) as ctx:
            click.echo(report.get_help(ctx))
        print("\n"+ str(e) + "\n")
    except UserConfigException as e:
        with click.Context(report) as ctx:
            click.echo(report.get_help(ctx))
        print("\nError with YAML file: "+ str(e) + "\n")
    except FileNotFoundError as e:
        with click.Context(report) as ctx:
            click.echo(report.get_help(ctx))
        print("\n"+ str(e) + "\n")
