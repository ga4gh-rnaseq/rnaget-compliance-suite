# -*- coding: utf-8 -*-
"""Module compliance_suite.functions.general.py

General functions to be used throughout library/application
"""

import sys

from compliance_suite.config.constants import *
from compliance_suite.config.tests import *

def get_longest_testname_length():
    """Return the longest test name from the test dictionary
    
    Returns:
        (str): longest test name
    """

    return max([len(a) for a in TESTS_DICT.keys()])