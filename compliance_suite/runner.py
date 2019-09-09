# -*- coding: utf-8 -*-
"""Module compliance_suite.runner.py

This module contains Runner class, which is responsible for creating and
running all test nodes associated with one server outlined in the user config 
file. Tests are created for all object types (projects, studies, expressions) 
and API routes.
"""

import datetime
import logging
import re
import sys

import compliance_suite.functions.general as gf
from compliance_suite.config.tests import TESTS_DICT as tests_config_dict
from compliance_suite.config.tests import TESTS_BY_OBJECT_TYPE as tests_by_obj
from compliance_suite.config.tests import NOT_IMPLEMENTED_TESTS_BY_OBJECT_TYPE \
    as not_impl_tests_by_obj
from compliance_suite.config.graph import TEST_GRAPH as graph
from compliance_suite.config.graph import NOT_IMPLEMENTED_TEST_GRAPH as \
    not_impl_graph
import compliance_suite.config.constants as c
from compliance_suite.node import Node

class Runner():
    """Runs all tests for one server, generates report accordingly

    The TestRunner class is used to run tests for a single server in the config
    file. It runs tests, sets test status to pass/fail/skip, passes context
    variables through the test graphs and generate JSON report appropriately.

    Attributes:
        root (Test): Test instance at the base/root of test graph
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
        retrieved_server_settings (dict): holds information about server-side
            supported filters/formats to inform subsequent test cases
        
    """

    def __init__(self, server_config):
        """instantiate a TestRunner object

        Args:
            server_config (dict): all relevant configs for a single server from
                the user config YAML
        """

        self.root = None
        self.total_tests = 0
        self.total_tests_passed = 0
        self.total_tests_failed = 0
        self.total_tests_skipped = 0
        self.total_tests_warning = 0
        self.server_config = server_config
        self.results = {endpoint: {} for endpoint in c.ENDPOINTS}
        self.headers = {}
        self.retrieved_server_settings = {
            resource: {"supp_filters": [], "exp_format": ""} 
            for resource in c.ENDPOINTS
        }
    
    def processed_func_descrp(self, text):
        """Cleanup test function docstring for output to JSON report
        
        Args:
            text (str): docstring/text to cleanup
        
        Returns:
            (str): cleaned docstring/text
        """

        return re.sub(' +', ' ', text.replace('\n', '')).strip()

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
                    'test_description': self.processed_func_descrp(
                        child.kwargs["name"]),
                    'text': child.to_echo(),
                    'message': child.message,
                    'description': child.description,
                    'parents': [str(parent) for parent in child.parents],
                    'children': [str(child) for child in child.children],
                    'warning': child.warning
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

        status_d = {1: "PASSED", -1: "FAILED", 0: "SKIPPED",
                    2: "UNKNOWN ERROR"}
        longest_testname = self.get_longest_testname_length()

        label = node.label + 1
        for child in node.children:
            if child.label == label:
                child.run(self)
                dots = "." * (longest_testname - len(str(child))) + "..."
                logging.info(str(child) + dots + status_d[child.result])
                sys.stdout.flush()
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
            'implemented': self.server_config["implemented"],
            'date_time': str(now),
            'test_results': self.results,
            'total_tests': self.total_tests,
            'total_tests_passed': self.total_tests_passed,
            'total_tests_skipped': self.total_tests_skipped,
            'total_tests_failed': self.total_tests_failed,
            'total_warnings': self.total_tests_warning
        }

        return report_object

    def initiate_tests(self):
        """Initiates test objects and generates test graphs for execution

        For each API object instance (a single project, study, or expression), a
        new test graph with its own base is set up. This graph represents the 
        full repertoire of tests to be run for the API object.
        
        Returns:
            (list): list of all base nodes/Test objects for all constructed 
                graphs 
        """

        # base dictionary, set up to hold all tests, separated by API object
        # type and then by instance
        test_obj_dict = {
            "projects": {},
            "studies": {},
            "expressions": {},
            "continuous": {}
        }
        
        test_bases = []

        # generate test graph from the config file
        def add_test_children(subtree, parent_key, obj_type, id_key):
            """recursively generate a test graph from the config file

            This method uses the graph config in 
            compliance_suite.config.graph.py to recursively assign parent/child
            relationships to all tests in a set, thereby constructing a graph
            where each test node can refer to its parent or children.

            Args:
                subtree (dict): subset of the test graph
                parent_key (str): key for parent test name at the root of the
                    subtree
                obj_type (str): object type (project, study, expression)
                id_key (str): the unique id for the object instance that this
                    test is constructed for
            """

            for child_key in subtree[parent_key].keys():
                test_obj_dict[obj_type][id_key][parent_key].add_child(
                    test_obj_dict[obj_type][id_key][child_key]
                )

                if len(subtree[parent_key][child_key]) > 0:
                    add_test_children(subtree[parent_key], child_key, obj_type,
                                    id_key)

        # For each object type and instance, create a test base and the full set
        # of tests. Assign pass, fail, skip text, then start the recursive 
        # method to construct the test graph
        # if an object type is not implemented, then check the endpoint for the
        # appropriate response code error.
        server_config = self.server_config

        for obj_type in c.ENDPOINTS:
            obj_instances = None
            test_list = None
            test_tree = None

            if server_config["implemented"][obj_type]:
                obj_instance_keys = c.TEST_RESOURCES[obj_type].keys()
                obj_instances = [c.TEST_RESOURCES[obj_type][k] \
                                 for k in obj_instance_keys]
                test_list = tests_by_obj[obj_type]
                test_tree = graph
            else:
                obj_instances = [{"id": "NA", "filters": {"version": "1.0"}}]
                test_list = not_impl_tests_by_obj[obj_type]
                test_tree = not_impl_graph

            for obj_instance in obj_instances:
                test_base = Node(**{"name": "base",
                                    "obj_type": "base", 
                                    "obj_instance": "base",
                                    "description": "root test node on which to "
                                                + "base test graph"})
                test_bases.append([obj_type, obj_instance["id"], test_base])
                test_obj_dict[obj_type][obj_instance["id"]] = \
                    {"base": test_base}

                for test_key in test_list:
                    kwargs = tests_config_dict[test_key]
                    kwargs["obj_type"] = obj_type
                    kwargs["obj_instance"] = obj_instance
                    test_obj = Node(**kwargs)
                    test_obj.set_pass_text(kwargs["pass_text"])
                    test_obj.set_fail_text(kwargs["fail_text"])
                    test_obj.set_skip_text(kwargs["skip_text"])
                    test_obj_dict[obj_type][obj_instance["id"]][kwargs["name"]]\
                        = test_obj
            
                add_test_children(test_tree[obj_type], "base", obj_type,
                                obj_instance["id"])

        return test_bases

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

        self.base_tests = self.initiate_tests()
        for obj_type, obj_id, base_test in self.base_tests:
            logging.info("starting tests for %s: %s" % (obj_type, obj_id))
            sys.stdout.flush()
            base_test.run(base_test)
            self.recurse_label_tests(base_test)
            self.recurse_run_tests(base_test)
            self.recurse_generate_json(obj_type, obj_id, base_test)
    
    def get_longest_testname_length(self):
        """Return the longest test name from the test dictionary
        
        Returns:
            (str): longest test name
        """

        return max([len(a) for a in tests_config_dict.keys()])
