import json
import requests
import loompy

expression_get_expect_cases = [

    
]

expression_search_expect_cases = [

]

def expression_get_case(content_case):
    result = {"status": 1, "message": ""}
    url = content_case.get_mature_url()
    c = content_case.case_params

    response = requests.get(url, headers=content_case.headers)
    response_json = response.json()
    download_url = response_json["URL"]
    r = requests.get(download_url, allow_redirects=True)
    filename = c["tempfile"]
    open(filename, 'wb').write(r.content)
    
    ds = loompy.connect(c["tempfile"])

    result = {"status": 1, "message": ""}
    et = "observed %s: %s doesn't match expected: %s" # error message template
    attr_checks = [
        ["GeneName", ds.ra.GeneName[c["i"]["r"]], c["o"]["GeneName"]],
        ["GeneID", ds.ra.GeneID[[c["i"]["r"]]], c["o"]["GeneID"]],
        ["Condition", ds.ca.Condition[[c["i"]["c"]]], c["o"]["Condition"]],
        ["Tissue", ds.ca.Tissue[[c["i"]["c"]]], c["o"]["Tissue"]],
        ["Sample", ds.ca.Sample[[c["i"]["c"]]], c["o"]["Sample"]],
        ["Value", ds[c["i"]["r"],c["i"]["c"]], c["o"]["Value"]]
    ]
    
    try:

        for attr_l in attr_checks:
            if attr_l[1] != attr_l[2]:
                raise Exception(et % (attr_l[0], attr_l[1], attr_l[2]))
    
    except Exception as e:
        result["status"] = -1
        result["message"] = str(e)
    
    return result

def expression_get(response):

    response_json = response.json()
    download_url = response_json["URL"]
    r = requests.get(download_url, allow_redirects=True)
    filename = "temp_rnaget.loom"
    open(filename, 'wb').write(r.content)

    result = {"status": 1, "message": ""}

    for case in expression_get_expect_cases:
        if result["status"] == 1:
            result = expression_get_case(filename, case)
    
    return result

def expression_search_case():
    pass

def expression_search(response):
    pass