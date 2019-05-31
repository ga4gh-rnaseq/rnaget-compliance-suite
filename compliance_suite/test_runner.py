# -*- coding: utf-8 -*-
"""Module compliance_suite.test_runner.py

This module contains TestRunner class, which is responsible for creating and
running all tests associated with one server outlined in the user config file.
Tests are created for all object types (projects, studies, expressions) and
API routes.
"""

import datetime
import re
import sys

from compliance_suite.tests import initiate_tests

def processed_func_descrp(text):
    """Cleanup test function docstring for output to JSON report
    
    Args:
        text (str): docstring/text to cleanup
    
    Returns:
        (str): cleaned docstring/text
    """

    return re.sub(' +', ' ', text.replace('\n', '')).strip()


class TestRunner():
    """Runs all tests for one server, generates report accordingly

    The TestRunner class is used to run tests for a single server in the config
    file. It runs tests, sets test status to pass/fail/skip, passes context
    variables through the test graphs and generate JSON report appropriately.

    Attributes:
        root (Test): Test instance at the base/root of test graph
        session_params (dict): variables used to run conditional tests
        total_tests (int): total number of tests, regardless of status
        total_tests_passed (int): total number of tests passed
        total_tests_failed (int): total number of tests failed
        total_tests_skipped (int): total number of tests skipped
        total_tests_failed (int): total number of tests failed
        total_tests_warning (int): total number of tests generated warning
        server_config (dict): sub-dictionary of the user config YAML, all
            relevant configs for a single server
        results (dict): dictionary of tests results for all object types
            (project, study, expression) and instances of those objects
        headers (dict): Additional HTTP headers for the requests
        
    """

    def __init__(self, server_config):
        """instantiate a TestRunner object

        Args:
            server_config (dict): all relevant configs for a single server from
                the user config YAML
        """

        self.root = None
        # TODO: remove session_params if we don't need
        self.session_params = {}
        self.total_tests = 0
        self.total_tests_passed = 0
        self.total_tests_failed = 0
        self.total_tests_skipped = 0
        self.total_tests_warning = 0
        self.server_config = server_config
        self.results = {"projects": {}, "studies": {}, "expressions": {}, "continuous": {}}
        self.headers = {}

    def recurse_label_tests(self, root):
        """recursively populate label attribute of test objects in graph

        This method labels the test case nodes and populates label parameter
        in test objects. ensures parents are run first no matter the shape of
        test graph

        Args:
            root (Test): test object node in the graph. When called recursively,
                the child node is passed as the new root node
        """

        label = root.label + 1
        for child in root.children:
            if label > child.label:
                self.total_tests = self.total_tests + 1
                child.label = label
            if len(child.children) != 0:
                self.recurse_label_tests(child)

    def recurse_generate_json(self, obj_type, obj_id, node):
        """recursively generate json for test objects in graph
        
        Generate the report according to the label set in above function by
        test_result_object s. It also populates other params of test_runner
        object

        Args:
            obj_type (str): the object type this test graph pertains to:
                project, study, or expression
            obj_id (str): the unique accession/identifier of the object. Used
                to differentiate tests run for two or more unique projects,
                studies, or expressions
            node (Test): test object node in the graph. When called recursively,
                the child node is passed as the new root node
        """

        label = node.label + 1
        for child in node.children:
            if child.label == label:
                test_result_object = {
                    'name': str(child),
                    'result': child.result,
                    'test_description': processed_func_descrp(
                        child.kwargs["name"]),
                    'text': child.to_echo(),
                    'parents': [str(parent) for parent in child.parents],
                    'children': [str(child) for child in child.children],
                    'warning': child.warning,
                    'edge_cases': child.case_outputs
                }
                if child.result == 1:
                    self.total_tests_passed = self.total_tests_passed + 1
                elif child.result == -1:
                    self.total_tests_failed = self.total_tests_failed + 1
                else:
                    self.total_tests_skipped = self.total_tests_skipped + 1
                if child.warning is True:
                    self.total_tests_warning = self.total_tests_warning + 1

                if obj_id not in self.results[obj_type].keys():
                    self.results[obj_type][obj_id] = []
                
                self.results[obj_type][obj_id].append(test_result_object)

                if len(child.children) != 0:
                    self.recurse_generate_json(obj_type, obj_id, child)

    def recurse_run_tests(self, node):
        """Recursively run tests for all tests in the test graph

        Runs the test graph according to the label set, starting with the root
        node.

        Args:
            node (Test): test object node in the graph. When called recursively,
                the child node is passed as the new node/Test to be run
        """

        label = node.label + 1
        for child in node.children:
            if child.label == label:
                print(str(child), file=sys.stderr)
                child.run(self)
        for child in node.children:
            if len(child.children) != 0:
                self.recurse_run_tests(child)

    def generate_final_json(self):
        """Generate final report object this session/server
        
        Returns:
            (dict): dictionary of all stats associated with tests run against
                the server
        """

        now = datetime.datetime.now()
        report_object = {
            'server_name': self.server_config["server_name"],
            'base_url': self.server_config["base_url"],
            'date_time': str(now),
            'test_results': self.results,
            'total_tests': self.total_tests,
            'total_tests_passed': self.total_tests_passed,
            'total_tests_skipped': self.total_tests_skipped,
            'total_tests_failed': self.total_tests_failed,
            'total_warnings': self.total_tests_warning
        }

        return report_object

    def run_tests(self):
        """Complete pipeline of running tests from bases through the graph
        
        The controller function of the test runner object. Defines the
        complete pipeline. There are multiple base tests for a single server.
        There is one base per project, study, or expression instance. For
        example, if the user requested that 2 projects, 3 studies, and 4
        expressions be tested on the server, then 9 base tests would exist
        for the TestRunner. All tests are run recursively, starting from the 
        base test for each graph.
        """

        self.base_tests = initiate_tests(self.server_config)
        for obj_type, obj_id, base_test in self.base_tests:
            base_test.run(base_test)
            self.recurse_label_tests(base_test)
            self.recurse_run_tests(base_test)
            self.recurse_generate_json(obj_type, obj_id, base_test)
