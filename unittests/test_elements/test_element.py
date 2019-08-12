# -*- coding: utf-8 -*-
"""Module unittests.test_functions.test_element.py"""

from compliance_suite.elements.element import Element

def test_as_json():

    e = Element()
    e.as_json()
    assert 1 == 1
