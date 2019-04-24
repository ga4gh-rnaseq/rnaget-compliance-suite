# Compliance suite HOWTO

## Compliance data

In order to run the compliance test suite, the server to be tested has to be pre-loaded with a specific test dataset. The following files, that can be found in the [`data`](compliance_suite/data) folder, contain all the required information:

*JSON objects*
- `studies.json`
- `projects.json`
- `expressions.json`

*Expression data*
- matrix.tsv
- matrix.loom

The JSON objects reflect the response object types of the different API endpoints (as mock data) and must be loaded unchanged. The `expressions.json` file contains JSON objects for several data formats. Only objects for the data formats supported by the server should be loaded.
The expression data files represent expressions matrices in different data formats. They can be injested either unchanged or passed through any additional ETL procedure depending on the backend implementation of the API server. Only data formats supported by the server should be considered.

## Troubleshooting

### Update CA certificates

If you get the following error:

```
...
requests.exceptions.SSLError: HTTPSConnectionPool(host='localhost', port=58852): Max retries exceeded with url: /rnaget/projects/bcc000624f151afc81a475a2fc4a68a5 (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1056)')))
```

You need to update the CA bundle used by the `requests` python library, either running the suite as:

``` 
REQUESTS_CA_BUNDLE=path/to/cabundle rnaget-compliance-suite ...
```

or exporting the `REQUESTS_CA_BUNDLE` environment variable and running the suite as usual. A CA bundle containing update CA certificates for CRG endpoints is distributed as part of this GitHub repository and is available at [`certs`](certs).