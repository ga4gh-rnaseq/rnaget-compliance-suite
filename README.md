[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Travis (.org) branch](https://img.shields.io/travis/ga4gh-rnaseq/rnaget-compliance-suite/master.svg?style=flat-square)](https://travis-ci.org/ga4gh-rnaseq/rnaget-compliance-suite)
[![Coverage Status](https://img.shields.io/coveralls/github/ga4gh-rnaseq/rnaget-compliance-suite.svg?style=flat-square)](https://coveralls.io/github/ga4gh-rnaseq/rnaget-compliance-suite)
[![Read the Docs](https://img.shields.io/readthedocs/rnaget-compliance-suite.svg?style=flat-square)](https://rnaget-compliance-suite.readthedocs.io/en/latest/)

# Rnaget Compliance Suite

Repository for the [rnaget API](https://github.com/ga4gh-rnaseq/schema) 
Compliance document and test suite and based on the [refget compliance suite](https://github.com/ga4gh/refget-compliance-suite).

## Installing the compliance suite

Installing the compliance suite require downloading (or cloning)
[the source](ihttps://github.com/ga4gh-rnaseq/rnaget-compliance-suite)
from GitHub and running setup.py

```bash
python setup.py install
```

## Running the compliance suite

The following will generate a HTML report for your server and serve said HTML. 
It will also generate a tarball locally of the report

```bash
rnaget-compliance report -c user_config.yaml --serve
```

The following will generate a JSON report of your server:

```bash
rnaget-compliance report -c user_config.yaml --json server.json
```

Setting `--json -` will have the compliance suite write the JSON to STDOUT.

## Setting up the user config YAML file

The application receives information about what servers, projects, studies,
and expressions to query from the user config yaml file (-c). Below is a 
template of what this config file should look like:

```
servers:
  - server_name: Server A
    base_url: https://felcat.caltech.edu/rnaget/
    token: gd3uhUnyk3pVVDakkPSK7Pa0V7EvuOCa
    implemented:
        projects: true
        studies: true
        expressions: true
    projects:
      - id: 43378a5d48364f9d8cf3c3d5104df560
        filters:
          version: 1.0
          name: PCAWG
    studies:
      - id: 6cccbbd76b9c4837bd7342dd616d0fec
        filters:
          version: 1.0
          name: PCAWG
    expressions:
      - id: 2a7ab5533ef941eaa59edbfe887b58c4
        filters:
          studyID: 6cccbbd76b9c4837bd7342dd616d0fec
```

The yaml file requires a single root element "servers" under which multiple
server definitions can be listed. The program will query, in sequence, each
defined server. Multiple projects, studies, and expressions can be queried for a single server.

Accepted parameters for each server definition are as follows:

| Field       | Required | Description |
| ----------- | -------- | ----------- |
| server_name | Yes      | A unique name for the server, used to identify each server in report  |
| base_url    | Yes      | The base URL at which to access the API |
| token       | Optional | Bearer access token if required by data provider |
| implemented | Optional | Indicate which endpoint(s) (projects, studies, expressions) are implemented by the server. If an endpoint is implemented, all tests will be run for routes pertaining to it. If not, the program will expect a "not implemented" (501) response. If this parameter is not provided in the user config, all endpoints are assumed to be implemented. |
| projects    | Optional | Required if projects endpoint is implemented. List multiple projects to be queried by the program. Each project requires an "id" at which it can be retrieved, and a key:value listing of filter names and expected values under "filters." Filters will be applied to determine if the project can be retrieved via the search route. |
| studies     | Optional | Required if studies endpoint is implemented. List multiple studies to be queried by the program. Each study requires an "id" and "filters." |
| expressions | Optional | Required if expressions endpoint is implemented. List multiple expressions to be queried by the program. Each expression requires an "id" and "filters." |

An example user config file can be found in [user_config_template.yaml](https://github.com/ga4gh-rnaseq/rnaget-compliance-suite/blob/master/user_config_template.yaml).

## Example report output

An example of the json and html reports can be found in
[report](https://github.com/ga4gh-rnaseq/rnaget-compliance-suite/tree/master/report).
