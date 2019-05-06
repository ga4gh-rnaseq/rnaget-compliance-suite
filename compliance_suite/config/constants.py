import requests

HTTP_GET = 0
HTTP_POST = 1

REQUEST_METHOD = [
    requests.get,
    requests.post
]

ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.rnaget.v1.0.0+json'
}

SCHEMA_RELATIVE_DIR = "schemas"
SCHEMA_FILE_PROJECT = "rnaget-project.json"
SCHEMA_FILE_STUDY = "rnaget-study.json"
SCHEMA_FILE_EXPRESSION = ""
SCHEMA_FILE_PROJECT_ARRAY = "rnaget-project-array.json"

PROJECT_API = 'projects/'
STUDY_API = 'studies/'
EXPRESSION_API = "expressions/"
