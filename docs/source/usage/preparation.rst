Data preparation and getting started
====================================

Overview of server setup
------------------------

An RNAGet-compliant service serves RNAseq datasets through API routes and 
messages that match the specification. An RNAGet server should serve, and 
therefore contain, the following content:

*  Expression matrix and signal intensity files (eg. loom, tsv) via /expressions and /continuous routes. Matrices should be able to be subsetted via slicing operations.
*  Information pertaining to all studies relating to the expression data. It is assumed all samples in a study have been processed uniformly
*  Information pertaining to all projects relating to the studies.

The RNAGet specification therefore proposes a hierarchical data model in which
expression matrix and signal intensity data is associated with studies, and 
therefore projects (project -> study -> expression matrix and signal intensity).
Expression matrix files should be uploaded in one or more of the commonly used RNASeq
formats (loom, tsv, hd5, etc). Associated study and project information can be 
stored in any format (ie database or flat files), as long as the served content
matches the RNAGet specification.

**Note:** We strongly recommend that servers that implement the RNAGet specification
maintain the hierarchical data model of projects, studies, expressions, and 
continuous endpoints. However, if a dataset does not include one or more of these
object types, it is possible to create an RNAGet compliant server that leaves 
API routes for non-existent data unimplemented.

Preparing an API for RNAGet compliance
--------------------------------------

In general, the compliance application makes a series of http requests to a 
server specified by the user. The app makes requests to all API routes defined
in the specification (ie. requests all routes related to /projects, /studies,
/expressions, /continuous). For each tested route, the application checks
whether the http response has the correct content type and status code according to the spec.

Most importantly, the response body is validated against a JSON schema for the 
expected API route. For example, if a request is made for a specific project,
then the response body (in JSON format) should return all required fields for
a project object according to the spec.

If a test case passes these 3 checks (content type, status code, schema validation), 
the test passes.

To ensure an API is compliant according to the specification and testing suite,
the API must respond with the correct content type, status code, and JSON 
object/message schema for each route. The following table gives an overview of
the expected responses for each route.

Before running the compliance suite, it would be good practice to ensure the
server serves content according to the following routes and schemas.

.. csv-table:: Expected response by route
   :header: "Route", "Content Type", "Status Code", "Schema"
   :widths: 1 20 30 20

   "/projects/<id>", "`Default Encoding`_", "200 if project with id exists, 404 if not", "`Project`_"
   "/projects/search", "`Default Encoding`_", "200 (see `About Arrays`_)", "`Project Array`_"
   "/projects/search/filters", "`Default Encoding`_", "200", "`Search Filter Array`_"
   "/studies/<id>", "`Default Encoding`_", "200 if study with id exists, 404 if not", "`Study`_"
   "/studies/search", "`Default Encoding`_", "200 (see `About Arrays`_)", "`Study Array`_"
   "/studies/search/filters", "`Default Encoding`_", "200", "`Search Filter Array`_"
   "/expressions/<id>", "`Default Encoding`_", "200 if expression with id exists, 404 if not", "`Expression`_"
   "/expressions/formats", "`Default Encoding`_", "200", "`String Array`_"
   "/expressions/search", "`Default Encoding`_", "200 (see `About Arrays`_), 400 if format not specified", "`Expression Array`_"
   "/expressions/search/filters", "`Default Encoding`_", "200", "`Search Filter Array`_"
   "/continuous/<id>", "For loom files: application/vnd.loom; For tsv files: text/tab-separated-values", "200 if continuous with id exists, 404 if not", "None (response not in JSON)"
   "/continuous/formats", "`Default Encoding`_", "200", "`String Array`_"
   "/continuous/search", "`Default Encoding`_", "200 (see `About Arrays`_), 400 if format not specified", "`Continuous Array`_"
   "/continuous/search/filters", "`Default Encoding`_", "200", "`Search Filter Array`_"

Schemas
-------

In the table above, each route is associated with a JSON schema that responses
to that route must match. This section indicates the required properties for
each schema. The service must serve responses that fit the appropriate schema 
to pass the compliance tests.

Project
#######

A JSON object representing a **project**. The project must contain the field *id*,
representing project id, and can optionally specify *version*, *tags*, *name*,
and *description*. See the `specification <https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_ for more details.

An example **project**:
::
    {
        "description": "Pan Cancer Analysis of Whole Genomes test data from Expression Atlas E-MTAB-5423",
        "id": "43378a5d48364f9d8cf3c3d5104df560",
        "name": "PCAWG",
        "tags": [
            "PCAWG",
            "cancer"
        ],
        "version": "1.0"
    }

Project Array
#############

A JSON array, where each object in the array must be a **project**.

An example **project array**:
::
    [
        {
            "name": "PCAWG",
            "id": "43378a5d48364f9d8cf3c3d5104df560",
            "tags": [
                "PCAWG",
                "cancer"
            ],
            "description": "Pan Cancer Analysis of Whole Genomes test data from Expression Atlas E-MTAB-5423",
            "version": "1.0"
        }
    ]

Study
#####

A JSON object representing a **study**. The study must contain the field *id*,
representing study id, and can optionally specify *version*, *tags*, *name*, 
*description*, *parentProjectID*, *genome*, and *sampleList*. See the 
`specification <https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_ 
for more details.

An example **study**:
::
    {
        "name": "PCAWG",
        "id": "6cccbbd76b9c4837bd7342dd616d0fec",
        "parentProjectID": "43378a5d48364f9d8cf3c3d5104df560",
        "description": "PCAWG study",
        "tags": [
            "PCAWG",
            "cancer"
        ],
        "version": "1.0"
    }

Study Array
###########

A JSON array, where each object in the array must be a **study**.

An example **study array**:
::
    [
        {
            "name": "PCAWG",
            "id": "6cccbbd76b9c4837bd7342dd616d0fec",
            "parentProjectID": "43378a5d48364f9d8cf3c3d5104df560",
            "description": "PCAWG study",
            "tags": [
                "PCAWG",
                "cancer"
            ],
            "version": "1.0"
        }
    ]

Expression
##########

A JSON object representing an **expression**. The expression requires the
following fields:

* *id*: expression id
* *units*: Units for expression values (ie TPM, FPKM, counts)
* *URL*: URL to download the file

In addition, an expression can optionally specify *version*, *tags*, *fileType*, 
and *studyID*. See the 
`specification <https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_ 
for more details.

An example **expression**:
::
    {
        "id": "2a7ab5533ef941eaa59edbfe887b58c4",
        "units": "TPM",
        "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
        "URL": "http://woldlab.caltech.edu/~sau/rnaget/E-MTAB-5423-query-results.tpms.loom",
        "fileType": "loom"
    }

Expression Array
################

A JSON array, where each object in the array must be an **expression**.

An example **expression array**:
::
    [
        {
            "id": "2a7ab5533ef941eaa59edbfe887b58c4",
            "units": "TPM",
            "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
            "URL": "http://woldlab.caltech.edu/~sau/rnaget/E-MTAB-5423-query-results.tpms.loom",
            "fileType": "loom"
        }
    ]

Continuous
##########

A JSON object representing a **continuous** object. The continuous object must
contain the following fields:

* *id*: representing object id
* *URL*: URL to download file

Additionally, a continuous object can optionally specify *version*, *tags*,
*fileType*, and *studyID*. See the 
`specification <https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_ 
for more details.

**Note:** continuous objects are served only by the /continuous/search endpoint.
The /continuous/<id> endpoint serves the continuous data as a file attachment
rather than a JSON object.

An example **continuous** object:
::
    {
        "URL": "/woldlab/castor/home/sau/public_html/rnaget/signal-query-results.loom",
        "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
        "tags": [
            "cancer"
        ],
        "fileType": "loom",
        "version": "1.0",
        "id": "fa057c6d18c44960a1b8b49d065b3889"
    }

Continuous Array
################

A JSON array, where each object in the array must be a *continuous* object.

An example **continuous array**:
::
    [
        {
            "URL": "/woldlab/castor/home/sau/public_html/rnaget/signal-query-results.loom",
            "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
            "tags": [
                "cancer"
            ],
            "fileType": "loom",
            "version": "1.0",
            "id": "fa057c6d18c44960a1b8b49d065b3889"
        }
    ]

Search Filter
#############

A JSON object representing a **search filter**, which indicates which URL 
parameters/keys can be used to filter search results for projects, studies, 
expressions, or continuous objects. A **search filter** must specify the following
fields:

* *filter*: filter name to use in search query URL
* *fieldType*: data type of values for this filter
* *description*: description of the filter

A search filter can optionally specify *values*, an array of supported values
for this filter. See the `specification
<https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_ for more details.

An example **search filter**
::
    {
        "fieldType": "string",
        "values": [
            "1.0"
        ],
        "description": "version to search for",
        "filter": "version"
    }

Search Filter Array
###################

A JSON array, where each object in the array must be a **search filter**.

An example **search filter array**:
::
    [
        {
            "fieldType": "string",
            "values": [
                "1.0"
            ],
            "description": "version to search for",
            "filter": "version"
        }
    ]

String Array
############

An array of strings, represented in JSON.

An example **string array**
::
    ["loom", "tsv", "hd5"]

Notes
-----

Default Encoding
################

The table of expected responses by API route indicates that most routes should
return JSON, and therefore one of the default content types. The default content
types are:

* application/vnd.ga4gh.rnaget.v1.0.0+json
* application/json

About Arrays
############

JSON arrays are returned for requests made to the various "search" routes 
(/projects/search, /studies/search, etc). Unless requests made to this route 
are improperly formatted, responses should generally have a status code of 200.
Even in cases where request search parameters do not match any object, the 
response body should be an empty array, and the status code should be 200. In
other words, requests made to a search endpoint should never yield a 404 not
found error, even if no objects were found via search criteria.

Next Steps
----------

Once the server of interest conforms to the above guidelines (data 
uploaded and routes configured) as well as the requirements laid out in the
specification, the RNAget compliance suite can be installed and run against the
server. The `next article <installation.html>`_ provides instructions on how to install the 
compliance app.
