import json
import os

import requests

# Some variables for not repeating the same thing

PROJECT_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.rnaget.v1.0.0+json'
}
PROJECT_API = 'projects/'
PROJECT_ID = 'bcc000624f151afc81a475a2fc4a68a5'
PROJECT_VERSION = '1.0'


def project_get(test, runner):
    '''
    Test to check if project endpoint returns 200 using test project id 
    and appropriate accept headers
    '''
    base_url = str(runner.base_url)
    for header_name, header_value in runner.headers.items():
        PROJECT_ACCEPT_HEADER[header_name] = header_value
    response = requests.get(base_url + PROJECT_API + PROJECT_ID,
                            headers=PROJECT_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def project_get_default(test, runner):
    '''
    Test to check if project endpoint returns 200 using test project id 
    and no accept headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + PROJECT_API +
                            PROJECT_ID, headers=runner.headers)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def project_search(test, runner):
    '''
    Test to check if project search endpoint returns 200 searching for 
    all projects with appropriate accept headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + PROJECT_API + 'search',
                            headers=PROJECT_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def project_search_url_params(test, runner):
    '''
    Test to check if project search endpoint returns 200 searching 
    by URL parameters with appropriate accept headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + PROJECT_API + 'search?version=' + PROJECT_VERSION,
                            headers=PROJECT_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def project_search_url_params_cases(test, runner):
    '''
    Test to check if project search endpoint behaves correctly searching
    by several different URL parameters cases with appropriate accept headers
    '''
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _query = case[0]
        _status_code = case[1][0]
        _elems = case[1][1]
        response = requests.get(base_url + PROJECT_API + 'search' + _query,
                                headers=PROJECT_ACCEPT_HEADER)
        case_output_object = {'api': PROJECT_API + 'search:' +
                              _query + ':' + str(PROJECT_ACCEPT_HEADER), 'code': _status_code, 'items': _elems}
        if response.status_code == _status_code and len(response.json()) == _elems:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_outputs.append(case_output_object)


def project_search_filters(test, runner):
    '''
    Test to check if project search filter endpoint returns 200 
    with appropriate accept headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + PROJECT_API + 'search/filters',
                            headers=PROJECT_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1
