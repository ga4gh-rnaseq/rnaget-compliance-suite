# -*- coding: utf-8 -*-
"""Module compliance_suite.elements.element.py

This module contains the TestElement class, an abstract representation of
some component relating to a compliance test. Test elements can be further
subdivided as a TestExecutor, Component, or Case
"""

class Element(object):
    """Abstract representation of some element of a compliance test"""
    
    def as_json(self):
        """Return all test result information as json"""

        pass