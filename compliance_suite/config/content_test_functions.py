import json
import requests
import loompy
import os


def expression_content_test(function):
    def wrapper(content_case):
        result = {"status": 1, "message": ""}
        url = content_case.get_mature_url()
        c = content_case.case_params
        request_params = {}
        if "request_params_func" in c.keys():
            request_params = c["request_params_func"](content_case)

        try:

            print(url)
            print(request_params)
            print("***")

            response = requests.get(url, headers=content_case.headers, params=request_params)
            response_json = response.json()
            download_url = c["download_url"](response_json)
            r = requests.get(download_url, allow_redirects=True)
            file_write = open(c["tempfile"], 'wb')
            file_write.write(r.content)
            file_write.close()

            result = function(content_case)
        except Exception as e:
            result["status"] = -1
            result["message"] = ["Message", "Error parsing expression json and download url"]

        return result

    return wrapper

@expression_content_test
def expression_get_case(content_case):
    c = content_case.case_params
    message = ["Message", "Asserting contents of expression matrix, row %s, column %s" % ( str(c["i"]["r"]), str(c["i"]["c"]))]
    result = {"status": 1, "message": message}

    try: 
        ds = loompy.connect(c["tempfile"])
        et = "observed %s: %s doesn't match expected: %s" # error message template
        attr_checks = [
            ["GeneName", ds.ra.GeneName[c["i"]["r"]], c["o"]["GeneName"]],
            ["GeneID", ds.ra.GeneID[[c["i"]["r"]]], c["o"]["GeneID"]],
            ["Condition", ds.ca.Condition[[c["i"]["c"]]], c["o"]["Condition"]],
            ["Tissue", ds.ca.Tissue[[c["i"]["c"]]], c["o"]["Tissue"]],
            ["Sample", ds.ca.Sample[[c["i"]["c"]]], c["o"]["Sample"]],
            ["Value", ds[c["i"]["r"],c["i"]["c"]], c["o"]["Value"]]
        ]

        for attr_l in attr_checks:
            if attr_l[1] != attr_l[2]:
                raise Exception(et % (attr_l[0], attr_l[1], attr_l[2]))
    
    except Exception as e:
        result["status"] = -1
        result["message"] = ["Message", str(e)]
    finally:
        ds.close()
        os.remove(c["tempfile"])
    
    return result

@expression_content_test
def expression_search_case(content_case):
    c = content_case.case_params
    params = c["request_params_func"](content_case.test, content_case.runner)

    slice_params = ["featureNameList", "sampleIDList"]

    for slice_param in slice_params:
        if slice_param in c.keys():
            params[slice_param] = ",".join(c[slice_param])

    message = ["Message", str(params)]
    result = {"status": 1, "message": message}
    filename = c["tempfile"]
    ds = None

    try:
        ds = loompy.connect(filename)    
        genenames = ds.ra.GeneName
        geneids = ds.ra.GeneID
        conditions = ds.ca.Condition
        samples = ds.ca.Sample
        tissues = ds.ca.Tissue
        print("From temp loom:")
        print(genenames)
        print(geneids)
        print(conditions)
        print(samples)
        print(tissues)
        
        if "featureNameList" in c.keys():
            if len(genenames) != len(c["featureNameList"]):
                raise Exception("# of rows in matrix: %s does not equal featureNameList length: %s" % (len(genenames), len(c["featureNameList"])))
            if "-".join(sorted(genenames)) != "-".join(sorted(c["featureNameList"])):
                raise Exception("Matrix gene names do not match featureNameList")
        
        if "sampleIDList" in c.keys():
            if len(samples) != len(c["sampleIDList"]):
                raise Exception("# of columns in matrix: %s does not equal sampleIDList length: %s" % (len(genenames), len(c["sampleIDList"])))
            if "-".join(sorted(samples)) != "-".join(sorted(c["sampleIDList"])):
                raise Exception("Matrix sample IDs do not match sampleIDList")

    except Exception as e:
        result["status"] = -1
        result["message"] = ["Message", str(e)]
    finally:
        if ds:
            ds.close()
        if os.path.exists(filename):
            os.remove(filename)

    return result
