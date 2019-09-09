# -*- coding: utf-8 -*-
"""Module compliance_suite.cli.py

This module contains the report generation entry point and associated methods
for the RNAGet compliance testing suite. Command line arguments are parsed
and validated before the TestRunner tests are initiated. JSON report is written
to file and a local server serving the report can be spun up if user specifies.
"""

import shutil
import time
import json
import os
import sys
import tarfile
import logging
import inspect

import click
import compliance_suite
from compliance_suite.report_server import ReportServer
from compliance_suite.runner import Runner
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
@click.option('--output_dir', '-o', default='rnaget-compliance-results', 
              help='path to output results/web archive directory')
@click.option('--serve', is_flag=True, help='spin up a server')
@click.option('--uptime', '-u', default='3600',
              help='time that server will remain up in seconds')
@click.option('--no-tar', is_flag=True, help='skip the creation of a tarball')
@click.option('--force', '-f', is_flag=True, 
              help="force overwrite of output directory")
def report(user_config, output_dir, serve, uptime, no_tar, force):
    """Program entrypoint. Executes compliance tests and generates report

    This method parses the CLI command 'report' to execute the report session
    and generate report on terminal, html file and json file if provided by the
    user

    Arguments:
        user_config (str): Required. Path to user config YAML file
        output_dir (str): Optional. Path to output directory
        serve (bool): Optional. If true, spin up a server
        uptime (int): Optional. How long report server remains up in seconds
        no_tar (bool): Optional. If true, do not create .tar.gz of output dir
        force (bool): Optional. If true, overwrite output dir if it exists 
    """

    final_json = []
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    logging.addLevelName(9, "SUCCESS")
    logging.info("starting RNAGet compliance testing")
    
    try:

        # check that the user config has been specified, if not, program
        # cannot proceed with tests
        if not user_config:
            raise ArgumentException(
                'No user config file provided. Specify path to yaml file with '
                + '-c'
            )

        logging.info("parsing config file: " + user_config)
        sys.stdout.flush()
        
        # check that the server uptime is a valid integer
        if not uptime.isdigit():
            raise ArgumentException('Server uptime is not a valid integer.')

        # parse the user config and check it for any errors, raising errors
        # as necessary
        user_config = UserConfigParser(user_config)
        user_config.parse_config_file()
        user_config.validate_config_file()

        # validate the specified archive path is ok to write to
        output_dirname = os.path.basename(output_dir)
        output_base_dir = os.path.dirname(output_dir)
        if output_base_dir == "":
            output_dir = "./" + output_dirname
            output_base_dir = "."

        # raise error if base directory does not exist (program will not
        # create parent directories)
        if not (os.path.exists(output_base_dir)):
            raise FileNotFoundError("cannot create output directory at " 
                                    + output_dir + ", base directory "
                                    + output_base_dir + " does not exist")
        
        # raise error if specified archive directory already exists
        if not force:
            if os.path.exists(output_dir) or \
                os.path.exists(output_dir + ".tar.gz"):
                raise ArgumentException("cannot create output directory at " 
                                        + output_dir + ", directory/archive "
                                        + "already exists")
        
        # if force, delete the output directory so it can be overwritten 
        if force and os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        # create the output archive, and copy the web files there
        template_web_dir = os.path.join(
            os.path.dirname(compliance_suite.report_server.__file__), 'web')
        shutil.copytree(template_web_dir, output_dir)

        # for each server in the user config, create a Runner
        # run associated tests and add the resulting JSON to the final json
        # report
        for server_config in user_config.d["servers"]:
            tr = Runner(server_config)

            token = None
            if "token" in server_config.keys():
                token = server_config["token"]

            if token:
                tr.headers['Authorization'] = 'Bearer ' + str(token)
            logging.info("starting tests for server: " 
                         + str(server_config["server_name"]))
            sys.stdout.flush()
            tr.run_tests()
            final_json.append(tr.generate_final_json())

        scan_for_errors(final_json)

        # write results.json to output directory
        with open(os.path.join(output_dir, 'results.json'), 'w+') as outfile:
            json.dump(final_json, outfile)
        
        logging.info("all tests complete, results json available at %s/%s" %(
            output_dir, 'results.json'
        ))

        # write tar.gz archive of report and web files if user specified
        if not no_tar:
            logging.info("creating gzipped tarball of results directory")

            with tarfile.open(
                output_dir + '.tar.gz', "w:gz"
            ) as tar:
                tar.add(output_dir, arcname=os.path.basename(output_dirname))
            logging.info("gzipped tarball of results directory available "
                         + "at " + output_dir + ".tar.gz")

        # start server if user specified --serve
        server = ReportServer(output_dir)
        server.render_html()

        if serve is True:
            logging.info("serving results as HTML report from output " 
                         + "directory " + output_dir)
            server.set_free_port()
            server.serve_thread(uptime=int(uptime))
        else:
            logging.info("Report results can be served as HTML from results "
                         + "directory " + output_dir + ". (python3) -> "
                         + "python -m http.server 8000 OR (python2) -> python "
                         + "-m SimpleHTTPServer 8000")
            
    # handle various exception classes, each time printing the usage
    # instructions to terminal along with a description of what went wrong
    except ArgumentException as e:
        with click.Context(report) as ctx:
            click.echo(report.get_help(ctx))
        print("\n"+ str(e) + "\n")
        sys.exit(1)
    except UserConfigException as e:
        with click.Context(report) as ctx:
            click.echo(report.get_help(ctx))
        print("Error with YAML file: "+ str(e) + "\n")
        sys.exit(1)
    except FileNotFoundError as e:
        with click.Context(report) as ctx:
            click.echo(report.get_help(ctx))
        print("\n"+ str(e) + "\n")
        sys.exit(1)
