import json
import requests
import loompy

expect_cases = [
    {
        "i": {
            "r": 1,
            "c": 10
        },
        "o": {
            "GeneID": "Foo",
            "GeneName": "Bar",
            "Col": "Condition Sample Tissue",
            "value": 22
        }
    }
]

def expression_get_case(filename, c):
    ds = loompy.connect(filename)

    result = {"status": 1, "message": ""}
    et = "observed %s: %s doesn't match expected: %s" # error message template
    attr_checks = [
        ["GeneName", ds.ra.GeneName[c["i"]["r"]], c["o"]["GeneName"]],
        ["GeneID", ds.ra.GeneID[[c["i"]["r"]]], c["o"]["GeneID"]]
    ]
    
    try:

        for attr_l in attr_checks:
            if attr_l[1] != attr_l[2]:
                raise Exception(et % (attr_l[0], attr_l[1], attr_l[2]))

        # print(ds.ra.GeneName[case["i"]["r"]])
        # 
        # print(ds.ca.Condition[case["i"]["c"]])
        # print(ds.ca.Sample[case["i"]["c"]])
        # print(ds.ca.Tissue[case["i"]["c"]])
    
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

    for case in expect_cases:
        if result["status"] == 1:
            result = expression_get_case(filename, case)
    
    return result