import requests
import json

# Some variables for not repeating the same thing

STUDY_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.rnaget.v1.0.0+json'
}
STUDY_API = 'studies'


def study_implement(test, runner):
    '''
    Test to check if study-endpoint returns 200 OK with appropriate headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + STUDY_API, headers=STUDY_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def study_implement_default(test, runner):
    '''
    Test to check if study-endpoint returns 200 OK without headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + STUDY_API)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1
