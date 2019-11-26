# -*- coding: utf-8 -*-
"""Module compliance_suite.functions.content_testing.py

Functions to execute file attachment/content testing with. Each content testing
function in this module should accept a ContentCase class object and modify it,
adding to its audit logs and assigning an error if one is encountered. These
functions must return a dictionary indicating function status, so that the
ContentCase can be updated with the status.
"""

import json
import requests
import loompy
import os
import re
import numpy
from compliance_suite.functions.attribute_handlers import ATTRIBUTE_HANDLERS
from compliance_suite.functions.general import sanitize_dict

def download_attachment(function):
    """Decorator for content tests that involve file attachment dload

    Decorates a content test function with preliminary workup steps 
    (initial request for expression/continuous object, downloading file 
    attachment, etc.)

    Arguments:
        function (function): inner function
    
    Returns:
        (function): inner function decorated with outer function
    """

    def wrapper(content_case):
        """Inner function returned by the decorator function

        Arguments:
            content_case (ContentCase): content case object for test case
        
        Returns:
            (dict): test case result
        """

        # assign url and request params
        result = {"status": 1, "message": ""}
        c = content_case.case_params

        try:

            matrix_bytes = c["download_func"](content_case)
            if os.path.exists(c["tempfile"]):
                os.remove(c["tempfile"])

            file_write = open(c["tempfile"], 'wb')
            file_write.write(matrix_bytes)
            file_write.close()

            # get the attribute handler based on object type and file format
            obj_type = content_case.test.kwargs["obj_type"]
            server_settings = content_case.runner.retrieved_server_settings
            fmt = server_settings[obj_type]["exp_format"]
            attribute_handler = ATTRIBUTE_HANDLERS[obj_type][fmt](c["tempfile"])
            content_case.set_attribute_handler(attribute_handler)

            # execute the inner function
            result = function(content_case)

        # if any exception is encountered in the above process, the test fails
        # and the reason should be displayed in the report
        except Exception as e:
            result["status"] = -1
            content_case.set_error_message("Error parsing expression json and "
                + "download url: " + str(e))
            content_case.append_audit(str(e))
        finally:
            if os.path.exists(c["tempfile"]):
                os.remove(c["tempfile"])

        return result

    return wrapper

@download_attachment
def expression_value_test_case(content_case):
    """Assertion function for 'Expression Get' Content test cases

    Arguments:
        content_case (ContentCase): content case object for test case
    
    Returns:
        (dict): test case result
    """

    c = content_case.case_params
    ah = content_case.attribute_handler
    result = {"status": 1, "message": ""}

    try:
        et = "observed %s: %s doesn't match expected: %s" # error template

        # six checks: GeneName, GeneID, Condition, Tissue, Sample, Value
        # for each sub-list, the first elem is the key,
        # the second elem is the actual value in the matrix
        # the third elem is the expected output according to test case 
        attr_checks = [
            ["GeneName", ah["GeneName"][c["i"]["r"]], c["o"]["GeneName"]],
            ["GeneID", ah["GeneID"][c["i"]["r"]], c["o"]["GeneID"]],
            ["Condition", ah["Condition"][c["i"]["c"]], c["o"]["Condition"]],
            ["Tissue", ah["Tissue"][c["i"]["c"]], c["o"]["Tissue"]],
            ["Sample", ah["Sample"][c["i"]["c"]], c["o"]["Sample"]],
            ["Value", ah["Value"][c["i"]["r"],c["i"]["c"]], c["o"]["Value"]]
        ]

        # check that the observed value in the matrix matches the expected,
        # if not, raise an error
        for attr_l in attr_checks:
            content_case.append_audit(
                "Asserting observed %s(s) match expected" % (attr_l[0]))
            if attr_l[1] != attr_l[2]:
                raise Exception(et % (attr_l[0], attr_l[1], attr_l[2]))
    
    except Exception as e:
        result["status"] = -1
        result["message"] = ["Message", str(e)]
        content_case.set_error_message(str(e))
    finally:
        if ah["FH"]:
            ah["FH"].close()
        if os.path.exists(c["tempfile"]):
            os.remove(c["tempfile"])
    
    return result

@download_attachment
def expression_slice_test_case(content_case):
    """Assertion function for 'Expression Search' Content test cases

    Arguments:
        content_case (ContentCase): content case object for test case
    
    Returns:
        (dict): test case result
    """

    c = content_case.case_params
    ah = content_case.attribute_handler
    
    # map search filters to the attributes they affect in the downloaded matrix
    # eg. the featureIDList filter affects what GeneIDs will be returned 
    attr_d = {
        "featureIDList": {"tbl_attr": "GeneID", "row/col": "row"},
        "featureNameList": {"tbl_attr": "GeneName", "row/col": "row"},
        "sampleIDList": {"tbl_attr": "Sample", "row/col": "column"}
    }

    # map minExpression/maxExpression search filters to functions that assess
    # whether they are functioning correctly
    # values with minExpression should all be greater/equal than threshold
    # values with maxExpression should all be less/equal than threshold
    expr_d = {
        "minExpression": {
            "cmp_func": lambda value, threshold: value >= threshold,
            "s": "above"
        },
        "maxExpression": {
            "cmp_func": lambda value, threshold: value <= threshold,
            "s": "below"
        }
    }

    result = {"status": 1, "message": ""}

    try:
        # featureIDList, featureNameList, sampleIDList
        for slice_key in sorted(attr_d.keys()):

            if slice_key in c.keys():
                content_case.append_audit(
                    "asserting number of %ss matches number of supplied %ss" % (
                        attr_d[slice_key]["row/col"],
                        attr_d[slice_key]["tbl_attr"]
                    )
                )

                # if minExpression or maxExpression is part of supplied params,
                # this will further pare down the returned columns and we
                # cannot expect columns to be identical to sampleIDList
                if (slice_key == "sampleIDList") and \
                ("minExpression" in c.keys() or "maxExpression" in c.keys()):
                    set_requested = set(c[slice_key])
                    set_returned = set(ah[attr_d[slice_key]["tbl_attr"]])
                    set_difference = set_returned.difference(set_requested)
                    
                    content_case.append_audit(
                        "Requested: " + str(set_requested))
                    content_case.append_audit(
                        "Returned: " + str(set_returned))
                    content_case.append_audit(
                        "Difference: " + str(set_difference))
                    content_case.append_audit(
                        "Difference Length: " + str(len(set_difference)))

                    if len(set_difference) != 0:
                        exc_message = "There are additional " \
                          + attr_d[slice_key]["row/col"] + "s returned in the "\
                          + "matrix compared to the request %s" % slice_key
                        raise Exception(exc_message)

                # otherwise, we expect the returned matrix rows or columns
                # to EXACTLY match the request 
                # (featureIDList or featureNameList for rows,
                #  sampleIDList for columns)
                else:
                    if len(ah[attr_d[slice_key]["tbl_attr"]]) != \
                       len(c[slice_key]):
                        
                        exc_message = "" \
                        + "# of matrix %ss: " % (attr_d[slice_key]["row/col"]) \
                        + str(len(ah[attr_d[slice_key]["tbl_attr"]])) \
                        + " does not equal %s length: " % slice_key \
                        + str(len(c[slice_key])) + ". " \
                        + "Matrix %ss: " % (attr_d[slice_key]["row/col"]) \
                        + str(ah[attr_d[slice_key]["tbl_attr"]]) + " " \
                        + slice_key + ": " + str(c[slice_key])
                        
                        raise Exception(exc_message)
                    
                    content_case.append_audit(
                        "asserting returned %ss match supplied %ss" % (
                            attr_d[slice_key]["tbl_attr"],
                            attr_d[slice_key]["tbl_attr"]
                        )
                    )
                    if "-".join(sorted(ah[attr_d[slice_key]["tbl_attr"]])) != \
                    "-".join(sorted(c[slice_key])):
                        exc_message = "Matrix %ss do not match %s" % (
                            attr_d[slice_key]["tbl_attr"], slice_key
                        )
                        raise Exception(exc_message)
        
        # minExpression, maxExpression
        for e_key in sorted(expr_d.keys()):
            if e_key in c.keys():
                s, cmp_func = expr_d[e_key]["s"], expr_d[e_key]["cmp_func"]

                content_case.append_audit(
                    "asserting expression values are %s %s threshold" % (
                        s, e_key))

                genes = [elem["featureName"] for elem in c[e_key]]
                gene_row_d = {ah["GeneName"][i]: i 
                              for i in range(0, len(ah["GeneName"]))
                              if ah["GeneName"][i] in set(genes)}
                gene_thresholds_d = {elem["featureName"]: elem["threshold"] \
                                     for elem in c[e_key]}
                
                # each column of the matrix must have ALL genes that
                # satisfy minExpression/maxExpression threshold. ALL genes
                # must satisfy their respective threshold, as multiple genes
                # provided to minExpression/maxExpression will return 
                # the INTERSECTION of columns
                for col in range(0, len(ah["Sample"])):

                    # check all genes with thresholds to see if the value
                    # is greater than the threshold. If any gene is not within
                    # the threshold, set status to -1 (fail) 
                    fail_gene = ""
                    for gene in genes:
                        row = gene_row_d[gene]
                        threshold = float(gene_thresholds_d[gene])
                        value = float(ah["Value"][row, col])
                        content_case.append_audit(
                            "Checking %s value: %s " % (gene, str(value))
                            + "is %s threshold %s" % (s, str(threshold))
                        )

                        if not cmp_func(value, threshold):
                            fail_gene = gene
                            exc_message = \
                                "Gene %s NOT %s %s" % (fail_gene, s, e_key) \
                                + " threshold at column %s" % (str(col))
                            raise Exception(exc_message)

    except Exception as e:
        result["status"] = -1
        result["message"] = ["Message", str(e)]
        content_case.set_error_message(str(e))
    finally:
        if ah["FH"]:
            ah["FH"].close()
        if os.path.exists(c["tempfile"]):
            os.remove(c["tempfile"])
    return result

@download_attachment
def continuous_test_case(content_case):
    """Assertion function for Continuous Get and Search Content test cases

    Arguments:
        content_case (ContentCase): content case object for test case
    
    Returns:
        (dict): test case result
    """

    c = content_case.case_params
    ah = content_case.attribute_handler
    result = {"status": 1, "message": ""}

    try:
        # there are 3 sub-assertions to continuous get content testing
        # 1. assert_values: observed track, position, values MUST match expected
        # 2. chr: if chr parameter is specified, all positions MUST have the 
        #         same chr
        # 3. start/end: if start and/or end is specified, all positions MUST
        #               fall within the start/end range (first position must)
        #               greater than or equal to request start, last position
        #               must be less than request end)

        # sub-assertion 1: assert_values
        if "assert_values" in c.keys():
            for assert_obj in c["assert_values"]: # assert the correct val
                                                  # of multiple row/col/cells
                a = assert_obj
                row, col = [a["i"]["r"], a["i"]["c"]]

                # assert correct track (row), position (column), cell value
                assertions_l = [
                    ["Track", ah["Track"][row], a["o"]["Track"]],
                    ["Position", ah["Position"][col], a["o"]["Position"]],
                    ["Value", round(float(ah["Value"][row, col]), 3),
                              round(float(a["o"]["Value"]), 3)]
                ]

                for asst in assertions_l: # assertion
                    content_case.append_audit(
                        "asserting observed %s: %s " % (asst[0], str(asst[1]))
                        +  "equals expected: %s" % str(asst[2])
                    )
                    if asst[1] != asst[2]:
                        exc_message = \
                            "observed %s: %s " % (asst[0], str(asst[1])) \
                            + "DOES NOT equal expected: %s" % str(asst[2])
                        raise Exception(exc_message)
        
        # sub-assertion 2: chr
        if "chr" in c.keys():
            content_case.append_audit("asserting returned chromosome matches "
                + "request")

            # get a set of unique chromosomes from the matrix
            # there MUST be 1 chr in the set, and it must match the request
            base_chr_set = set([p.split(":")[0] for p in ah["Position"]])
            obs_chr = list(base_chr_set)[0]

            if len(base_chr_set) != 1:
                raise Exception("More than 1 chromosome in continuous file")
            
            if obs_chr != c["chr"]:
                raise Exception("chr in continuous file: %s " % obs_chr
                    + "DOES NOT match request 'chr' parameter: %s" % c["chr"])
        
        # sub-assertion 3: start/end
        if "start" in c.keys() or "end" in c.keys():
            bases_range = [int(p.split(":")[1]) for p in ah["Position"]]
            start_base = min(bases_range)
            end_base = max(bases_range)

            assertions = {
                "start": {
                    "observed": start_base,
                    "function": lambda observed, limit: observed >= limit,
                    "desc": "greater than or equal to"

                }, "end": {
                    "observed": end_base,
                    "function": lambda observed, limit: observed < limit,
                    "desc": "less than"
                }
            }

            for akey in ["start", "end"]: # assertion key
                if akey in c.keys():
                    obs, func, desc = [assertions[akey][k] for k in \
                                      ["observed", "function", "desc"]]
                    lim = int(c[akey]) # limit/threshold ie value in the request
                    
                    content_case.append_audit("asserting %s position is " % akey
                        + "%s request '%s' parameter" % (desc, akey))
                    
                    if not func(obs, lim):
                        exc_message = "observed %s: %s is " % (akey, str(obs)) \
                            + "NOT %s requested %s: %s" % (desc, akey, str(lim))
                        raise Exception(exc_message)
    
    except Exception as e:
        result["status"] = -1
        content_case.set_error_message(str(e))
    finally:
        if ah["FH"]:
            ah["FH"].close()
        if os.path.exists(c["tempfile"]):
            os.remove(c["tempfile"])

    return result