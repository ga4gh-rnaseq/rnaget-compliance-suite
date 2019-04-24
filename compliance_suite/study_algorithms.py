import json

import requests

# Some variables for not repeating the same thing

STUDY_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.rnaget.v1.0.0+json'
}
STUDY_API = 'studies/'
STUDY_ID = '0a5c41465e7072eb24b53436be64f191'
STUDY_VERSION = '1.0'


def study_get(test, runner):
    '''
    Test to check if study-endpoint returns 200 using test study id 
    and appropriate accept headers
    '''
    base_url = str(runner.base_url)
    for header_name, header_value in runner.headers.items():
        STUDY_ACCEPT_HEADER[header_name] = header_value
    response = requests.get(base_url + STUDY_API +
                            STUDY_ID, headers=STUDY_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def study_get_default(test, runner):
    '''
    Test to check if study-endpoint returns 200 using test study id 
    and no accept headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + STUDY_API +
                            STUDY_ID, headers=runner.headers)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def study_search(test, runner):
    '''
    Test to check if study search endpoint returns 200 searching for 
    all studys with appropriate accept headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + STUDY_API + 'search',
                            headers=STUDY_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def study_search_url_params(test, runner):
    '''
    Test to check if study search endpoint returns 200 searching 
    by URL parameters with appropriate accept headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + STUDY_API + 'search?version=' + STUDY_VERSION,
                            headers=STUDY_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def study_search_url_params_cases(test, runner):
    '''
    Test to check if study search endpoint behaves correctly searching 
    by several different URL parameters cases with appropriate accept headers
    '''
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _query = case[0]
        _status_code = case[1][0]
        _elems = case[1][1]
        response = requests.get(base_url + STUDY_API + 'search' + _query,
                                headers=STUDY_ACCEPT_HEADER)
        case_output_object = {'api': STUDY_API + 'search:' +
                              _query + ':' + str(STUDY_ACCEPT_HEADER)}
        if response.status_code == _status_code and len(response.json()) == _elems:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_outputs.append(case_output_object)


def study_search_filters(test, runner):
    '''
    Test to check if study search filter endpoint returns 200 
    with appropriate accept headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + STUDY_API + 'search/filters',
                            headers=STUDY_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1
