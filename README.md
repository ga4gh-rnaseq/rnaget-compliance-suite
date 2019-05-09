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

Multiple projects, studies, and expressions can be queried for a single server
by listing object id and filters below the appropriate heading. To query
multiple servers, list multiple server configurations below "servers". The 
"token" attribute is only required if the data holder requires 
authentication/authorization.

An example user config file can be found in [user_config_template.yaml](https://github.com/ga4gh-rnaseq/rnaget-compliance-suite/blob/ja_new_test_cases/user_config_template.yaml).

## Example report output

An example of the json and html reports can be found in
[report](https://github.com/ga4gh-rnaseq/rnaget-compliance-suite/tree/master/report).
