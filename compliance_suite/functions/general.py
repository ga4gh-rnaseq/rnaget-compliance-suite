# -*- coding: utf-8 -*-
"""Module compliance_suite.functions.general.py

General functions to be used throughout library/application
"""

import sys

def sanitize_dict(d):
    """Remove/omit secure information from a dictionary

    Arguments:
        d (dict): dictionary containing potentially sensitive info
    
    Returns:
        (dict): dictionary with sensitive info omitted
    """

    new_d = d.copy()
    sanitize_keys = ["Authorization"]
    for k in sanitize_keys:
        if k in new_d.keys():
            new_d[k] = "omitted"
    return new_d

    

    