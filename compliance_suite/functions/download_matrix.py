import json
import requests
from compliance_suite.functions.general import sanitize_dict

def download_from_ticket(content_case):

    c = content_case.case_params

    ticket_url = content_case.get_mature_url()
    ticket_params = c["request_params_func"](content_case)

    content_case.append_audit("Ticket URL: " + ticket_url)
    content_case.append_audit("Params: " + str(sanitize_dict(ticket_params)))
    ticket_response = requests.get(
        ticket_url, params=ticket_params, headers=content_case.headers,
        allow_redirects=True)

    ticket_json = json.loads(ticket_response.content)

    matrix_url = ticket_json["url"]
    matrix_headers = ticket_json["headers"] \
                     if "headers" in ticket_json.keys() \
                     else {}
    
    matrix_response = requests.get(
        matrix_url, headers=matrix_headers, allow_redirects=True)
    return matrix_response.content

def download_from_bytes(content_case):
    c = content_case.case_params
    bytes_url = content_case.get_mature_url()
    bytes_params = c["request_params_func"](content_case)
    content_case.append_audit("Bytes URL: " + bytes_url)
    content_case.append_audit("Params: " + str(sanitize_dict(bytes_params)))
    bytes_response = requests.get(
        bytes_url, params=bytes_params, headers=content_case.headers,
        allow_redirects=True)
    return bytes_response.content
