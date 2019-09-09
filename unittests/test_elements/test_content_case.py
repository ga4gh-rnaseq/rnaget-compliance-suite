# -*- coding: utf-8 -*-
"""Module unittests.test_elements.test_content_case.py"""

from compliance_suite.elements.content_case import ContentCase
from unittests.methods import *

def test_content_case_success():
    success_cases = [
        {"name": "Expression Get Content 1"},
        {"name": "Continuous Get Content, Assert Correct Values, 1"},
        {"name": "Continuous Get Content, chr, start, and end, 1"}
    ]

    for success_case in success_cases:
        runner, node, case_params = get_runner_node_case_params_by_case(
            success_case["name"])
        runner.retrieved_server_settings["expressions"]["exp_format"] = "loom"
        runner.retrieved_server_settings["continuous"]["exp_format"] = "loom"
        content_case = ContentCase(case_params, node, runner)
        content_case.execute_test_case()
        assert content_case.status == 1

def test_content_case_failures():
    failure_cases = [
        {
            "name": "Expression Get Content 1",
            "replace": {
                "url": "expressions/ecf875d885658ec8c7f17c9c1377037b"
            },
            "message": "observed Value: 100.0 doesn't match expected: 0.0"
        },

        {
            "name": "Slice by featureIDList",
            "replace": {
                "url": "expressions/964c54b974cba66cc2cecabf874f2de5"
            },
            "message": "# of matrix rows: 1 does not equal featureIDList "
                + "length: 3. Matrix rows: ['ENSG00000037965'] "
                + "featureIDList: ['ENSG00000037965', 'ENSG00000243503', "
                + "'ENSG00000259285']"
        },

        {
            "name": "Slice by featureIDList",
            "replace": {
                "url": "expressions/9d0540df9b867404092bbf9d62d02648"
            },
            "message": "Matrix GeneIDs do not match featureIDList"
        },

        # {
        #     "name": "slice by featureIDList, sampleIDList, minExpression, "
        #         + "and maxExpression",
        #     "replace": {
        #         "url": "expressions/af0ab1d31e93a358f552adcc47dd4dc8"
        #     },
        #     "message": "There are additional columns returned in the matrix "
        #         + "compared to the request sampleIDList"
        # },

        # {
        #     "name": "Slice by minExpression",
        #     "replace": {
        #         "url": "expressions/599ffa32b4a673c48dcf82e1f5ad2126"
        #     },
        #     "message": "Gene CLIC1 NOT above minExpression threshold at "
        #         + "column 2"
        # },

        {
            "name": "Continuous Get Content, Assert Correct Values, 1",
            "replace": {
                "url": "continuous/89c1a7011f8201aeb39d9851bd8b868e"
            },
            "message": "observed Value: 100.0 DOES NOT equal expected: 8.904"
        },

        {
            "name": "Continuous Get Content, chr, 1",
            "replace": {
                "url": "continuous/de3d2567774ae951f84783c890504104"
            },
            "message": "More than 1 chromosome in continuous file"
        },

        {
            "name": "Continuous Get Content, chr, 1",
            "replace": {
                "url": "continuous/e614231a96d9ffefa21384d8f5227cd1"
            },
            "message": "chr in continuous file: chr5 DOES NOT match request "
                + "'chr' parameter: chr1"
        },

        {
            "name": "Continuous Get Content, chr, start, and end, 1",
            "replace": {
                "url": "continuous/6ccacf344f0f009cbcb19c31543daab2"
            },
            "message": "observed start: 25 is NOT greater than or equal to "
                + "requested start: 30"
        }
    ]

    for failure_case in failure_cases:
        runner, node, case_params = get_runner_node_case_params_by_case(
            failure_case["name"])
        runner.retrieved_server_settings["expressions"]["exp_format"] = "loom"
        runner.retrieved_server_settings["continuous"]["exp_format"] = "loom"
        content_case = ContentCase(case_params, node, runner)
        content_case.case_params.update(failure_case["replace"])
        content_case.execute_test_case()

        assert content_case.status == -1
        assert content_case.error_message == failure_case["message"]
