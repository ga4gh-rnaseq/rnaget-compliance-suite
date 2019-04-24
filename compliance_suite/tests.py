import sys

from compliance_suite.expression_algorithms import *
from compliance_suite.project_algorithms import *
from compliance_suite.study_algorithms import *


class Test():
    '''
    Test Case class. All the test cases are instances of this class.

    label - used in graph algorithms to label the test case graph
    algorithm - Strategy design pattern in used here. It is the underlying algorithm used in the test case
    result - 0 indicates skipped, 1 indicates passed, -1 indicates failed and 2 is not yet ran
    pass_text - text in the report when test case is passed
    skip_text - text in the report when test case is skipped
    fail_text - text in the report when test case is failed
    parents - dependencies of the test case to run
    children - test cases which have this test case as dependency
    warning - if the result of this test case is warning for the server implementation
    cases - multiple edge cases of same test object
    '''

    def __init__(self, algorithm):
        '''
        Initiates the Test Case object. Algorithm is a required field to initiate test case object
        '''
        self.label = 0
        self.algorithm = algorithm
        self.result = 2
        self.pass_text = ''
        self.fail_text = ''
        self.skip_text = ''
        self.parents = []
        self.children = []
        self.warning = False
        self.cases = []
        self.case_outputs = []

    def __str__(self):
        '''
        String repr of the test case
        '''
        return 'test_' + self.algorithm.__name__

    def set_pass_text(self, text):
        '''
        Setter for pass_text
        '''
        self.pass_text = text

    def set_fail_text(self, text):
        '''
        Setter for fail_text
        '''
        self.fail_text = text

    def set_skip_text(self, text):
        '''
        Setter for skip_text
        '''
        self.skip_text = text

    def generate_skip_text(self):
        '''
        Skip text is generated if there is no skip text (the case when test is skipped when the parent test cases fail or skip)
        To track down the root cause of this skip.
        '''
        text = str(self) + ' is skipped because '
        for test in self.parents:
            if test.result != 1:
                text = text + test.to_echo()
        return text

    def add_parent(self, parent_test_case):
        '''
        Adds a parent test case
        '''
        self.parents.append(parent_test_case)

    def add_child(self, child_test_case):
        '''
        Adds a child test case
        '''
        self.children.append(child_test_case)
        child_test_case.add_parent(self)

    def to_skip(self):
        '''
        Checks if any of the parent test cases failed or skipped which causes this case to skip
        '''
        for test in self.parents:
            if test.result != 1:
                print("{} - {}".format(str(test), str(test.result)), file=sys.stderr)
                return True
        return False

    def run(self, test_runner):
        '''
        First checks if the parent test cases were successful then run the text.
        '''
        # Checking if to skip
        if self.to_skip() is True:
            # warning will be generated because the test case is skipped because of some parent failure
            self.warning = True
            self.result = 0
            return
        # run the test if not skipped
        self.algorithm(self, test_runner)
        # if it fails it'll generate a warning
        if self.result == -1:
            self.warning = True

    def to_echo(self):
        '''
        Returns the text based on the result of the test case
        '''
        if self.result == 1:
            return self.pass_text
        elif self.result == -1:
            return self.fail_text
        elif self.result == 2:
            return 'Unknown error'
        elif self.skip_text == '':
            self.skip_text = self.generate_skip_text()
        return self.skip_text


def initiate_tests():
    '''
    Initiates test case objects and generates a test case graph for execution
    '''

    def base_algorithm(test, runner):
        if True is True:
            test.result = 1

    # Base test case
    test_base = Test(base_algorithm)

    # Project Success Test Cases

    test_project_implement = Test(project_get)
    test_project_implement.set_pass_text(
        'Project endpoint implemented by the server')
    test_project_implement.set_fail_text(
        'Project endpoint not implemented by the server')

    test_project_implement_default = Test(project_get_default)
    test_project_implement_default.set_pass_text(
        'Project endpoint implemented with default encoding')
    test_project_implement_default.set_fail_text(
        'Project endpoint not implemented with default encoding')

    test_project_search = Test(project_search)
    test_project_search.set_pass_text(
        'Projects can be retrieved through the search endpoint')
    test_project_search.set_fail_text(
        'Projects cannot be retrieved through the search endpoint')

    test_project_search_url_params = Test(project_search_url_params)
    test_project_search_url_params.set_pass_text(
        'Projects can be retrieved using URL parameters through the search endpoint')
    test_project_search_url_params.set_fail_text(
        'Projects cannot be retrieved using URL parameters through the search endpoint')

    test_project_search_url_params_cases = Test(
        project_search_url_params_cases)
    test_project_search_url_params_cases.set_pass_text(
        'Projects can be retrieved using URL parameters through the search endpoint for all cases')
    test_project_search_url_params_cases.set_fail_text(
        'Projects cannot be retrieved using URL parameters through the search endpoint for all cases')
    test_project_search_url_params_cases.cases = [
        ('?version=2.0', [404, None]),
        ('?tags=PCAWG,cancer', [200, 1]),
        ('?tags=single-cell', [404, None]),
        ('?foo=bar', [404, None])
    ]

    test_project_search_filters = Test(project_search_filters)
    test_project_search_filters.set_pass_text(
        'Project filters can be retrieved through the search endpoint')
    test_project_search_filters.set_fail_text(
        'Project filters be retrieved through the search endpoint')

    # Study Success Test Cases

    test_study_implement = Test(study_get)
    test_study_implement.set_pass_text(
        'Study endpoint implemented by the server')
    test_study_implement.set_fail_text(
        'Study endpoint not implemented by the server')

    test_study_implement_default = Test(study_get_default)
    test_study_implement_default.set_pass_text(
        'Study endpoint implemented with default encoding')
    test_study_implement_default.set_fail_text(
        'Study endpoint not implemented with default encoding')

    test_study_search = Test(study_search)
    test_study_search.set_pass_text(
        'Studies can be retrieved through the search endpoint')
    test_study_search.set_fail_text(
        'Studies cannot be retrieved through the search endpoint')

    test_study_search_url_params = Test(study_search_url_params)
    test_study_search_url_params.set_pass_text(
        'Studies can be retrieved using URL parameters through the search endpoint')
    test_study_search_url_params.set_fail_text(
        'Studies cannot be retrieved using URL parameters through the search endpoint')

    test_study_search_url_params_cases = Test(study_search_url_params_cases)
    test_study_search_url_params_cases.set_pass_text(
        'Studies can be retrieved using URL parameters through the search endpoint for all cases')
    test_study_search_url_params_cases.set_fail_text(
        'Studies cannot be retrieved using URL parameters through the search endpoint for all cases')
    test_study_search_url_params_cases.cases = [
        ('?version=2.0', [404, None]),
        ('?tags=PCAWG,cancer', [200, 1]),
        ('?tags=single-cell', [404, None]),
        ('?foo=bar', [404, None])
    ]

    # Expression endpoint test cases

    test_expression_implement = Test(expression_implement)
    test_expression_implement.set_pass_text('Expression endpoint implemented in the server')
    test_expression_implement.set_fail_text('Expression endpoint not implemented in the server')

    test_expression_implement_default = Test(expression_implement_default)
    test_expression_implement_default.set_pass_text('Expresion endpoint implemented with default encoding')
    test_expression_implement_default.set_fail_text('Expression endpoint not implemented with default encoding')

    # generating test graph

    test_base.add_child(test_project_implement)

    test_project_implement.add_child(test_project_implement_default)

    test_base.add_child(test_project_search)
    test_project_search.add_child(test_project_search_url_params)
    test_project_search.add_child(test_project_search_filters)
    test_project_search.add_child(test_project_search_url_params_cases)

    test_base.add_child(test_study_implement)

    test_study_implement.add_child(test_study_implement_default)

    test_base.add_child(test_study_search)
    test_study_search.add_child(test_study_search_url_params)
    test_study_search.add_child(test_study_search_url_params_cases)

    test_base.add_child(test_expression_implement)

    test_expression_implement.add_child(test_expression_implement_default)

    return test_base
