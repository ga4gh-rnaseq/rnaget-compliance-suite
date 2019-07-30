# -*- coding: utf-8 -*-
"""Module compliance_suite.node.py

This module contains Node class, which represents and houses information for a 
single test node within the test tree/runner. A single test node corresponds to
one API route, and one object associated with that route. Tests response status
and whether the returned JSON object matches the required schema.
"""

import sys

from compliance_suite.elements.executor import Executor

class Node():
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
        message (dict): json representation of test information, to be 
            displayed in report under case
        description (str): description of the test at this node
        parents (list): Test nodes that are higher in the test graph than this.
            ie. Dependencies for this Test
        children (list): Test nodes which have this Test as dependency
        warning (bool): if the result of this test case is warning for the
            server implementation
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
        self.message = {}
        self.description = kwargs["description"]
        self.parents = []
        self.children = []
        self.warning = False

        self.case_outputs = []

    def test_algorithm(self, test, runner):
        """Generalized algorithm for testing an API route and object

        All tests follow a consistent model. An API request is made, and the
        response is checked. If the response has a status code of 200, then
        the returned JSON object must match the expected object schema for the
        requested object. Individual test scenarios have different routes,
        expected responses, and schemas for returned data.

        Args:
            test (Node): this Node object
            runner (Runner): reference to Runner object that this test
                belongs to
        """

        # base tests automatically pass, but do not figure in the end report
        if self.kwargs["name"] == "base":
            self.result = 1
        # all true tests run through the Executor class
        else:
            executor = Executor(test, runner)
            executor.execute_tests()
            self.result = executor.status
            self.message = executor.as_json()

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
            test_runner (Runner): Runner instance associated with this
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
