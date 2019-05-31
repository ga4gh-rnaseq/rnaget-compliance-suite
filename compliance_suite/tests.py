# -*- coding: utf-8 -*-
"""Module compliance_suite.tests.py

This module contains Test class, which houses information for a single test
of the API. A single test corresponds to one API route, and one object
associated with that route. Tests response status and whether the returned
JSON object matches the required schema.
"""

import sys

from compliance_suite.single_test_executor import SingleTestExecutor as STE
from compliance_suite.config.tests import TESTS_DICT as tests_config_dict
from compliance_suite.config.tests import TESTS_BY_OBJECT_TYPE as tests_by_obj
from compliance_suite.config.tests import NOT_IMPLEMENTED_TESTS_BY_OBJECT_TYPE \
    as not_impl_tests_by_obj
from compliance_suite.config.graph import TEST_GRAPH as graph
from compliance_suite.config.graph import NOT_IMPLEMENTED_TEST_GRAPH as \
    not_impl_graph
from compliance_suite.config.constants import ENDPOINTS

class Test():
    """Run a single test of the API for one route and one object instance

    Test Case class. All the test cases are instances of this class.

    Attributes:
        kwargs (dict): keyword arguments containing information about base url,
            API route, and object instance (id, params, etc.)
        label (str): used in graph algorithms to label the test case graph
        algorithm (method): Strategy design pattern in used here. It is the
            underlying algorithm used in the test case
        result (int): 0 indicates skipped, 1 indicates passed,
            -1 indicates failed and 2 is not yet run
        pass_text (str): text in the report when test case is passed
        fail_text (str): text in the report when test case is failed
        skip_text (str): text in the report when test case is skipped
        parents (list): Test nodes that are higher in the test graph than this.
            ie. Dependencies for this Test
        children (list): Test nodes which have this Test as dependency
        warning (bool): if the result of this test case is warning for the
            server implementation
        cases (list): multiple edge cases of same test object
    """

    def __init__(self, **kwargs):
        """instantiate a Test object
        
        Args:
            kwargs (dict): keyword arguments about the test case/route to be
                assessed
        """

        self.kwargs = kwargs
        self.label = 0
        self.algorithm = self.test_algorithm
        self.result = 2
        self.pass_text = ''
        self.fail_text = ''
        self.skip_text = ''
        self.full_message = []
        self.parents = []
        self.children = []
        self.warning = False
        self.cases = []
        self.case_outputs = []

    def test_algorithm(self, test, runner):
        """Generalized algorithm for testing an API route and object

        All tests follow a consistent model. An API request is made, and the
        response is checked. If the response has a status code of 200, then
        the returned JSON object must match the expected object schema for the
        requested object. Individual test scenarios have different routes,
        expected responses, and schemas for returned data.

        Args:
            test (Test): this test object
            runner (TestRunner): reference to TestRunner object that this test
                belongs to
        """

        # base tests automatically pass, but do not figure in the end report
        if self.kwargs["name"] == "base":
            self.result = 1
        # all true tests run through the SingleTestExecution class
        else:
            ste = STE(self.get_mature_uri(runner, self.kwargs["uri"]),
                      self.kwargs["schema"], self.kwargs["http_method"],
                      self.kwargs["obj_instance"]["filters"], test, runner)
            ste.execute_test()

    def __str__(self):
        """String representation of the test case

        Returns:
            (str): name of the test case
        """
        return self.kwargs["name"]

    def set_pass_text(self, text):
        """Setter: set pass_text

        Args:
            text (str): to set to pass_text
        """
        self.pass_text = text

    def set_fail_text(self, text):
        """Setter: set fail_text

        Args:
            text (str): to set to fail_text
        """
        self.fail_text = text

    def set_skip_text(self, text):
        """Setter: set skip_text

        Args:
            text (str): to set to skip_text
        """
        self.skip_text = text

    def get_pass_text(self):
        """Getter: get pass_text

        Returns:
            (str): pass_text
        """
        return self.pass_text
    
    def get_fail_text(self):
        """Getter: get fail_text

        Returns:
            (str): fail_text
        """
        return self.fail_text
    
    def get_skip_text(self):
        """Getter: get skip_text

        Returns:
            (str): skip_text
        """
        return self.skip_text

    def generate_skip_text(self):
        """Generate text for skip message

        Skip text is generated if there is no skip text (the case when test is
        skipped when the parent test cases fail or skip).
        To track down the root cause of this skip.

        Returns:
            (str): generated skip text for the test
        """

        text = str(self) + ' is skipped because '
        for test in self.parents:
            if test.result != 1:
                text = text + test.to_echo()
        return text

    def add_parent(self, parent_test_case):
        """Add a parent test node to this test node

        Args:
            parent_test_case (Test): parent node of this test node in the graph
        """
        self.parents.append(parent_test_case)

    def add_child(self, child_test_case):
        """Add a child test node to this test node

        Args:
            child_test_case (Test): child node of this test node in the graph
        """
        self.children.append(child_test_case)
        child_test_case.add_parent(self)

    def to_skip(self):
        """Check parent tests for fails/skips which causes this test to skip

        If a parent test in the graph has failed or skipped, then this test 
        should skip as well.

        Returns:
            (bool): true if test will be skipped, false if test will be run
        """
        for test in self.parents:
            if test.result != 1:
                print("{} - {}".format(str(test), str(test.result)), 
                                       file=sys.stderr)
                return True
        return False

    def run(self, test_runner):
        """Check if test should be skipped, running if necessary

        This method first checks if the parent test cases were successful. If
        so, then the test will run. If the test fails, then a warning will be 
        set for this test

        Args:
            test_runner (TestRunner): TestRunner instance associated with this
                test
        """

        # Checking if to skip
        if self.to_skip() is True:
            # warning will be generated because the test case is skipped 
            # because of some parent failure
            self.warning = True
            self.result = 0
            return
        # run the test if not skipped
        self.algorithm(self, test_runner)
        # if it fails it'll generate a warning
        if self.result == -1:
            self.warning = True

    def to_echo(self):
        """Returns the text based on the result of the test case

        This method returns the appropriate text/message given the test result.
        If the test passed, pass_text will be returned, if test failed,
        fail_text will be returned, etc.

        Returns:
            (str): text/message appropriate to test result
        """
        if self.result == 1:
            return self.pass_text
        elif self.result == -1:
            return self.fail_text
        elif self.result == 2:
            return 'Unknown error'
        elif self.skip_text == '':
            self.skip_text = self.generate_skip_text()
        return self.skip_text
    
    def get_mature_uri(self, runner, immature_uri):
        """Returns full uri for an API route, replacing placeholders with ids

        This method constructs a true API route given server and object
        parameters in the user config file. The base url is added to the
        beginning of the route, and placeholders for project, study, and
        expression ids are replaced with true ids provided.

        Args:
            runner (TestRunner): TestRunner instance associated with this test
            immature_uri (str): uri without base url or placeholders replaced

        Returns:
            (str): mature uri with base url added and placeholders replaced
        """

        mature_uri = runner.server_config["base_url"]

        obj_type_placeholders = {
            "projects": "V_PROJECT_ID",
            "studies": "V_STUDY_ID",
            "expressions": "V_EXPRESSION_ID",
            "continuous": "V_CONTINUOUS_ID"
        }

        mature_uri += immature_uri.replace(
            obj_type_placeholders[self.kwargs["obj_type"]],
            self.kwargs["obj_instance"]["id"]
        )

        return mature_uri

def initiate_tests(server_config):
    """Initiates test objects and generates test graphs for execution

    For each API object instance (a single project, study, or expression), a
    new test graph with its own base is set up. This graph represents the full
    repertoire of tests to be run for the API object.

    Args:
        server_config (dict): sub dictionary of the user config YAML file,
            representing all parameters associated with one server
    
    Returns:
        (list): list of all base nodes/Test objects for all constructed graphs 
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

        This method uses the graph config in compliance_suite.config.graph.py
        to recursively assign parent/child relationships to all tests in a set,
        thereby constructing a graph where each test node can refer to its
        parent or children.

        Args:
            subtree (dict): subset of the test graph
            parent_key (str): key for parent test name at the root of the
                subtree
            obj_type (str): object type (project, study, expression)
            id_key (str): the unique id for the object instance that this test
                is constructed for
        """

        for child_key in subtree[parent_key].keys():
            test_obj_dict[obj_type][id_key][parent_key].add_child(
                test_obj_dict[obj_type][id_key][child_key]
            )

            if len(subtree[parent_key][child_key]) > 0:
                add_test_children(subtree[parent_key], child_key, obj_type,
                                  id_key)

    # For each object type and instance, create a test base and the full set of
    # tests. Assign pass, fail, skip text, then start the recursive method to
    # construct the test graph
    # if an object type is not implemented, then check the endpoint for the
    # appropriate response code error.

    for obj_type in ENDPOINTS:
        obj_instances = None
        test_list = None
        test_tree = None

        if server_config["implemented"][obj_type]:
            obj_instances = server_config[obj_type]
            test_list = tests_by_obj[obj_type]
            test_tree = graph
        else:
            obj_instances = [{"id": "NA", "filters": {"version": "1.0"}}]
            test_list = not_impl_tests_by_obj[obj_type]
            test_tree = not_impl_graph

        for obj_instance in obj_instances:
            test_base = Test(**{"name": "base",
                                "obj_type": "base", 
                                "obj_instance": "base"})
            test_bases.append([obj_type, obj_instance["id"], test_base])
            test_obj_dict[obj_type][obj_instance["id"]] = \
                {"base": test_base}

            for test_key in test_list:
                kwargs = tests_config_dict[test_key]
                kwargs["obj_type"] = obj_type
                kwargs["obj_instance"] = obj_instance
                test_obj = Test(**kwargs)
                test_obj.set_pass_text(kwargs["pass_text"])
                test_obj.set_fail_text(kwargs["fail_text"])
                test_obj.set_skip_text(kwargs["skip_text"])
                test_obj_dict[obj_type][obj_instance["id"]][kwargs["name"]]\
                    = test_obj
        
            add_test_children(test_tree[obj_type], "base", obj_type,
                            obj_instance["id"])

    return test_bases
