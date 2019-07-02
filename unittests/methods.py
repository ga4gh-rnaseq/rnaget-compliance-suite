# -*- coding: utf-8 -*-
"""Module unittests.unittests_methods.py

This module contains common methods to be accessed by multiple unit testing
modules.
"""

import os
import shutil
from unittests.constants import OUTPUT_DIR, OUTPUT_ARCHIVE

def copy_dict(d):
    """create copy of a dictionary

    Args:
        d (dict): dictionary to copy
    
    Returns:
        c (dict): copied dictionary, can be modified without affecting original
    """

    return {k: d[k] for k in d.keys()}

def copy_list(l):
    """create copy of a list

    Args:
        l (list): list to copy
    
    Returns:
        c (list): copied list, can be modified without affecting original
    """

    return [i for i in l]

def remove_output_dir():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    if os.path.exists(OUTPUT_ARCHIVE):
        os.remove(OUTPUT_ARCHIVE)