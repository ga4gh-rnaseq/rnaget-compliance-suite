import sys

from compliance_suite.config.constants import *
from compliance_suite.config.tests import *

def get_longest_testname_length():
    return max([len(a) for a in TESTS_DICT.keys()])