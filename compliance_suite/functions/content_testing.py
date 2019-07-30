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
import numpy

def loom_attribute_handler(input_file):
    """Attribute handler for loom files

    Supported file format may be different for each server, this function maps
    loom-specific attributes to a general data structure that can be used by
    all content testing functions regardless of file format

    Arguments:
        input_file (str): input loom file
    
    Returns:
        (dict): attribute handler, consistent structure regardless of file type 
    """

    # connects to the loom file, then remaps loom specific attributes to general
    # attribute names which are used in the content testing functions
    # eg. the loom-specific ds.ra.GeneID is mapped to dict["GeneID"]
    ds = loompy.connect(input_file)
    return {
        "GeneID": ds.ra.GeneID,
        "GeneName": ds.ra.GeneName,
        "Condition": ds.ca.Condition,
        "Tissue": ds.ca.Tissue,
        "Sample": ds.ca.Sample,
        "Value": ds
    }

def tsv_attribute_handler(input_file):
    """Attribute handler for tsv files

    Parses a tsv expression matrix, maps its attributes to a dictionary with
    consistent keys that can be used by all content testing functions
    
    Arguments:
        input_file (str): input tsv file
    
    Returns:
        (dict): attribute handler, consistent structure regardless of file type
    """

    gene_ids = []
    gene_names = []
    conditions = []
    tissues = []
    samples = []
    values = []

    inc = 0
    # open the tsv file
    for l in open(input_file, "r"):
        ls = l.rstrip().split("\t")

        if not l.startswith("#"): # ignore any starting comment lines if any
            if inc == 0: # column header line

                # using the column header line, assign the conditions, samples,
                # and tissues lists
                columns = ls[2:]
                samples = [column.split(", ")[0] for column in columns]
                n_col_split = len(columns[0].split(", "))
                if n_col_split > 1:
                    conditions = [column.split(", ")[1] for column in columns]
                    if n_col_split > 2:
                        tissues = [column.split(", ")[2] for column in columns]

            else: # data lines
                # each data line contains the gene id, gene name, and all 
                # expression values
                gene_ids.append(ls[0])
                gene_names.append(ls[1])
                values.append([float(v) for v in ls[2:]])

            inc += 1
    
    # return the populated values and attribute names under consistent keys
    return {
        "GeneID": gene_ids,
        "GeneName": gene_names,
        "Condition": conditions,
        "Tissue": tissues,
        "Sample": samples,
        "Value": numpy.matrix(values)
    }

ATTRIBUTE_HANDLER_BY_FORMAT = {
    "loom": loom_attribute_handler,
    "tsv": tsv_attribute_handler
}
"""maps format keywords to their attribute handler functions"""

def expression_content_test(function):
    """Decorator function for expressions-related content tests

    Decorates a content test function with preliminary workup steps 
    (initial request for expression object, downloading file attachment, etc.)

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
        url = content_case.get_mature_url()
        c = content_case.case_params
        request_params = {}
        if "request_params_func" in c.keys():
            request_params = c["request_params_func"](content_case)

        try:
            content_case.append_audit("Request URL: " + url)
            content_case.append_audit(
                "Request Headers:" + str(content_case.headers))
            content_case.append_audit("Request Params: " + str(request_params))

            # make the request for expression object, and get the download URL
            # from the "URL" property
            # write the file content to a temporary file for subsequent
            # content checking
            response = requests.get(url, headers=content_case.headers,
                params=request_params)
            content_case.append_audit("Response Body: " + str(response.text))
            response_json = response.json()
            download_url = c["download_url"](response_json)
            content_case.append_audit("Matrix Download URL: " + download_url)
            r = requests.get(download_url, headers=content_case.headers,
                allow_redirects=True)
            file_write = open(c["tempfile"], 'wb')
            file_write.write(r.content)
            file_write.close()

            # execute the inner function
            result = function(content_case)

        # if any exception is encountered in the above process, the test fails
        # and the reason should be displayed in the report
        except Exception as e:
            result["status"] = -1
            content_case.set_error_message("Error parsing expression json and "
                + "download url: " + str(e))
            content_case.append_audit(str(e))

        return result

    return wrapper

@expression_content_test
def expression_get_case(content_case):
    """Assertion function for 'Expression Get' Content test cases

    Arguments:
        content_case (ContentCase): content case object for test case
    
    Returns:
        (dict): test case result
    """

    c = content_case.case_params
    server_settings = content_case.runner.retrieved_server_settings
    result = {"status": 1, "message": ""}

    try:
        # parse expression matrix file and get the attribute handler based on
        # format
        fmt = server_settings["expressions"]["exp_format"]
        ah = ATTRIBUTE_HANDLER_BY_FORMAT[fmt](c["tempfile"])
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
        os.remove(c["tempfile"])
    
    return result

@expression_content_test
def expression_search_case(content_case):
    """Assertion function for 'Expression Search' Content test cases

    Arguments:
        content_case (ContentCase): content case object for test case
    
    Returns:
        (dict): test case result
    """

    c = content_case.case_params
    server_settings = content_case.runner.retrieved_server_settings
    # parse input file and get attribute handler according to 
    # expected file format
    fmt = server_settings["expressions"]["exp_format"]
    ah = ATTRIBUTE_HANDLER_BY_FORMAT[fmt](c["tempfile"]) # attribute handler
    
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
                    status = 1

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
                            status = -1
                    
                    if status != 1:
                        exc_message = \
                            "Gene %s NOT %s %s" % (fail_gene, s, e_key) \
                            + " threshold at column %s" % (str(col))
                        raise Exception(exc_message)

    except Exception as e:
        print("Expression Search Exception Encountered")
        result["status"] = -1
        result["message"] = ["Message", str(e)]
        content_case.set_error_message(str(e))
    finally:
        if os.path.exists(c["tempfile"]):
            os.remove(c["tempfile"])

    return result
