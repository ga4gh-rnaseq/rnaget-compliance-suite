import json
import requests
import loompy
import os
import numpy

def loom_attribute_handler(input_file):
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
    gene_ids = []
    gene_names = []
    conditions = []
    tissues = []
    samples = []
    values = []

    inc = 0
    for l in open(input_file, "r"):
        ls = l.rstrip().split("\t")

        if not l.startswith("#"):
            if inc == 0: # column header line
                columns = ls[2:]
                samples = [column.split(", ")[0] for column in columns]

                n_col_split = len(columns[0].split(", "))
                if n_col_split > 1:
                    conditions = [column.split(", ")[1] for column in columns]
                    if n_col_split > 2:
                        tissues = [column.split(", ")[2] for column in columns]
            else:
                gene_ids.append(ls[0])
                gene_names.append(ls[1])
                values.append([float(v) for v in ls[2:]])

            inc += 1
    
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

def expression_content_test(function):
    def wrapper(content_case):
        result = {"status": 1, "message": ""}
        url = content_case.get_mature_url()
        c = content_case.case_params
        request_params = {}
        if "request_params_func" in c.keys():
            request_params = c["request_params_func"](content_case)

        try:
            content_case.append_audit("Request URL: " + url)
            content_case.append_audit("Request Headers:" + str(content_case.headers))
            content_case.append_audit("Request Params: " + str(request_params))

            response = requests.get(url, headers=content_case.headers, params=request_params)
            content_case.append_audit("Response Body: " + str(response.text))
            response_json = response.json()
            download_url = c["download_url"](response_json)
            content_case.append_audit("Matrix Download URL: " + download_url)
            r = requests.get(download_url, headers=content_case.headers, allow_redirects=True)
            file_write = open(c["tempfile"], 'wb')
            file_write.write(r.content)
            file_write.close()
            result = function(content_case)

        except Exception as e:
            result["status"] = -1
            result["message"] = ["Message", "Error parsing expression json and download url"]
            content_case.set_error_message("Error parsing expression json and download url: "
                + str(e))
            content_case.append_audit(str(e))

        return result

    return wrapper

@expression_content_test
def expression_get_case(content_case):
    c = content_case.case_params
    message = ["Message", "Asserting contents of expression matrix, row %s, column %s" % ( str(c["i"]["r"]), str(c["i"]["c"]))]
    result = {"status": 1, "message": message}

    try: 
        fmt = content_case.runner.retrieved_server_settings["expressions"]["exp_format"]
        ah = ATTRIBUTE_HANDLER_BY_FORMAT[fmt](c["tempfile"]) # attribute handler
        
        et = "observed %s: %s doesn't match expected: %s" # error message template
        attr_checks = [
            ["GeneName", ah["GeneName"][c["i"]["r"]], c["o"]["GeneName"]],
            ["GeneID", ah["GeneID"][c["i"]["r"]], c["o"]["GeneID"]],
            ["Condition", ah["Condition"][c["i"]["c"]], c["o"]["Condition"]],
            ["Tissue", ah["Tissue"][c["i"]["c"]], c["o"]["Tissue"]],
            ["Sample", ah["Sample"][c["i"]["c"]], c["o"]["Sample"]],
            ["Value", ah["Value"][c["i"]["r"],c["i"]["c"]], c["o"]["Value"]]
        ]

        for attr_l in attr_checks:
            content_case.append_audit("Asserting observed %s(s) match expected" % (attr_l[0]))
            if attr_l[1] != attr_l[2]:
                raise Exception(et % (attr_l[0], attr_l[1], attr_l[2]))
    
    except Exception as e:
        result["status"] = -1
        result["message"] = ["Message", str(e)]
        content_case.set_error_message(str(e))
    finally:
        # ds.close()
        os.remove(c["tempfile"])
    
    return result

@expression_content_test
def expression_search_case(content_case):
    c = content_case.case_params
    fmt = content_case.runner.retrieved_server_settings["expressions"]["exp_format"]
    ah = ATTRIBUTE_HANDLER_BY_FORMAT[fmt](c["tempfile"]) # attribute handler
    
    attr_d = {
        "featureIDList": {
            "tbl_attr": "GeneID",
            "row/col": "row"

        },
        "featureNameList": {
            "tbl_attr": "GeneName",
            "row/col": "row"

        },
        "sampleIDList": {
            "tbl_attr": "Sample",
            "row/col": "column"

        }
    }

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
                    content_case.append_audit("Doing the other thing for sampleIDList")

                    set_requested = set(c[slice_key])
                    set_returned = set(ah[attr_d[slice_key]["tbl_attr"]])
                    set_difference = set_returned.difference(set_requested)
                    
                    content_case.append_audit("Requested: " + str(set_requested))
                    content_case.append_audit("Returned: " + str(set_returned))
                    content_case.append_audit("Difference: " + str(set_difference))
                    content_case.append_audit("Difference Length: " + str(len(set_difference)))

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
                    if len(ah[attr_d[slice_key]["tbl_attr"]]) != len(c[slice_key]):
                        content_case.append_audit("Making exception message")
                        content_case.append_audit("Foo")
                        
                        exc_message = "" \
                        + "# of matrix %ss: " % (attr_d[slice_key]["row/col"]) \
                        + str(len(ah[attr_d[slice_key]["tbl_attr"]])) \
                        + " does not equal %s length: " % slice_key \
                        + str(len(c[slice_key])) + ". " \
                        + "Matrix %ss: " % (attr_d[slice_key]["row/col"]) \
                        + str(ah[attr_d[slice_key]["tbl_attr"]]) + " " \
                        + slice_key + ": " + str(c[slice_key])

                        content_case.append_audit("Done exception message")
                        
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
                        content_case.append_audit("Checking %s value: %s is %s threshold: %s" % (gene, str(value), s, str(threshold)))
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
