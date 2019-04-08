import requests
import json

# Some variables for not repeating the same thing

PROJECT_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.rnaget.v1.0.0+json'
}
PROJECT_API = 'projects'


def project_implement(test, runner):
    '''
    Test to check if project-endpoint returns 200 OK with appropriate headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + PROJECT_API, headers=PROJECT_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def project_implement_default(test, runner):
    '''
    Test to check if project-endpoint returns 200 OK without headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + PROJECT_API)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1
