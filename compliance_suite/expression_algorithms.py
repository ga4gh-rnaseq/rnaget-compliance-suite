import requests
import json

# Some variables for not repeating the same thing

EXPRESSION_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.rnaget.v1.0.0+json'
}
EXPRESSION_API = 'expressions'


def expression_implement(test, runner):
    '''
    Test to check if expression-endpoint returns 200 OK with appropriate headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + EXPRESSION_API, headers=EXPRESSION_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def expression_implement_default(test, runner):
    '''
    Test to check if expression-endpoint returns 200 OK without headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + EXPRESSION_API)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1
