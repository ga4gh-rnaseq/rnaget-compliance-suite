# -*- coding: utf-8 -*-
"""Module unittests.test_functions.test_attribte_handlers.py"""

from compliance_suite.functions.attribute_handlers import *

def test_expression_tsv():

    input_file = "unittests/data/matrices/expressions/expression.tsv"
    ah = expression_tsv(input_file)

    assert len(ah["GeneID"]) == 100
    assert len(ah["GeneName"]) == 100
    assert len(ah["Sample"]) == 100

def test_continuous_tsv():

    input_file = "unittests/data/matrices/continuous/continuous.tsv"
    ah = continuous_tsv(input_file)