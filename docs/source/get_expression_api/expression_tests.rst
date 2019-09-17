Expression Tests
===================

This page outlines the success and failure criteria for all tests of Expression resources.

Expression API Tests
---------------------

Expression API tests assert the correct configuration of expression-related API 
routes. In order for a test case to succeed, the following conditions must be
met when evaluating the response:
    
    * For all cases, :code:`Content-Type` checking is enforced. The response **MUST** have a :code:`Content-Type` header of :code:`application/vnd.ga4gh.rnaget.v1.0.0+json` OR :code:`application/json`
    * For all cases, :code:`Status Code` checking is enforced. The response **MUST** have the expected status code
    * For all cases, schema checking is enforced. The json object in the response body **MUST** conform to a pre-defined schema of required fields and data types, which is specific to each API route

Expression API Test Cases
--------------------------

* `Get Test Expression`_
* `Expression Not Found`_
* `Get Supported Expression Formats`_
* `Expression Search Filters`_
* `Search Expressions by Format`_
* `Search Expressions With All Filters`_
* `Search Expressions With Single Filter, 1`_
* `Search Expressions With Single Filter, 2`_
* `Expression Search Filters Non-Matching Resources`_
* `Expression Search Format Not Specified`_
* `Expression Search Filetypes Match`_
* `Expression Search No Filetype Mismatches`_

Get Test Expression
####################
* **Route:** :code:`/expressions/<id>`
* **Description:** Requests test expression by its :code:`id`. Expects the returned expression to match the :code:`Expression` json schema.
* **Rationale:** Asserts that the :code:`/expressions/<id>` endpoint returns **one** valid expression object, with id matching the request.

* **Request:**

.. code-block:: python

   GET /expressions/ac3e9279efd02f1c98de4ed3d335b98e
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "id": "ac3e9279efd02f1c98de4ed3d335b98e",
     "version": "1.0",
     "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
     "url": "https://url/to/expression/file",
       "tags": [
         "RNAgetCompliance"
       ],
     "units": "TPM",
     "fileType": "loom/tsv"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is valid :code:`Expression` json
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT valid :code:`Expression` json

Expression Not Found
######################
* **Route:** :code:`/expressions/<id>`
* **Description:** Requests an expression with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Expression` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/expressions/<id>` endpoint does not return arbitrary :code:`Expression` objects, and only returns an :code:`Expression` when the :code:`id` matches.

* **Request:**

.. code-block:: python

   GET /expressions/nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 404 Not Found
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "Entry not found in database."
   }

* **Success Criteria:** :code:`Status Code == 404` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 404` OR response body is NOT valid :code:`Error` json

Get Supported Expression Formats
#################################
* **Route:** :code:`/expressions/formats`
* **Description:** Requests the available expression data file formats on the server. Expects an array of strings to be returned in the response body.
* **Rationale:** Asserts that :code:`/expressions/formats` returns an array of strings, indicating which expression file formats the server supports

* **Request:**

.. code-block:: python

   GET /expressions/formats
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     "loom",
     "tsv"
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is an array of strings in json format
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT an array of strings in json format

Expression Search Filters
###########################
* **Route:** :code:`/expressions/search/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Expressions`
* **Rationale:** Asserts that the endpoint returns an array of :code:`Search Filter` objects

* **Request:**

.. code-block:: python

   GET /expressions/search/filters
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "fieldType": "string",
       "values": [
         "1.0"
       ],
       "filter": "version",
       "description": "version to search for"
     },
     {
       "fieldType": "string",
       "filter": "studyID",
       "description": "parent studyID"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Search Filters`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Search Filters`

Search Expressions by Format
################################
* **Route:** :code:`/expressions/search`
* **Description:** Searches for all expressions, specifying only the required 'format' parameter. Expects an array of :code:`Expressions` in the response body.
* **Rationale:** Asserts that the :code:`/expressions/search` returns an array, and that each element in the array is an :code:`Expression`.

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "tags": [],
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "url": "/path/to/E-MTAB-5423-query-results.tpms.loom",
       "units": "TPM",
       "version": "1.0",
       "fileType": "loom"
     },
     {
       "tags": [
         "RNAgetCompliance"
       ],
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/expression.loom",
       "units": "TPM",
       "version": "1.0",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR :code:`Array Length < 1`

Search Expressions With All Filters
####################################
* **Route:** :code:`/expressions/search`
* **Description:** Searches expressions, using all filtering parameters associated with test expression. Expects an array of :code:`Expressions` to be returned in the response body. Array must contain at least 1 object.
* **Rationale:** Asserts that :code:`/expressions/search` returns an array of :code:`Expressions` even when specifying filters. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the test expression.

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "tags": [
         "RNAgetCompliance"
       ],
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/expression.loom",
       "units": "TPM",
       "version": "1.0",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR :code:`Array Length < 1`

Search Expressions With Single Filter, 1
#########################################
* **Route:** :code:`/expressions/search`
* **Description:** Searches expressions using only 1 filtering parameter associated with test expression (in addition to format). Expects an array of :code:`Expressions`, with length of 1 or greater.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields the test :code:`Expression` in the search results.

* **Requests:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "tags": [
         "RNAgetCompliance"
       ],
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/expression.loom",
       "units": "TPM",
       "version": "1.0",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR :code:`Array Length < 1`

Search Expressions With Single Filter, 2
#########################################
* **Route:** :code:`/expressions/search`
* **Description:** Searches expressions using only 1 filtering parameter (a different filter than above) associated with test expression (in addition to format). Expects an array of :code:`Expressions`, with length of 1 or greater.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields the test :code:`Expression` in the search results.

* **Requests:**

.. code-block:: python

   GET /expressions/search?format=loom&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "tags": [
         "RNAgetCompliance"
       ],
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/expression.loom",
       "units": "TPM",
       "version": "1.0",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR :code:`Array Length < 1`

Expression Search Filters Non-Matching Resources
#################################################
* **Route:** :code:`/expressions/search`
* **Description:** Tests that the expression search endpoint correctly filters out non-matching :code:`Expressions` based on url parameters. Makes a request to the :code:`/expressions/search` endpoint with invalid filters (not matching any :code:`Expression`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Expressions` that differ from filters.

* **Request:**

.. code-block:: python

   GET /expressions/search?format=nonexistentid9999999999999999999&version=nonexistentid9999999999999999999&studyID=nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT an empty array

Expression Search Format Not Specified
#######################################
* **Route:** :code:`/expressions/search`
* **Description:** Searches for all expressions WITHOUT specifying the required :code:`format` parameter. Expects a :code:`4xx` error response, with an error message indicating that the request was invalid.
* **Rationale:** As the :code:`format` parameter is required to specify file format for the :code:`/expressions/search` endpoint, this test asserts malformed requests raise an error.

* **Request:**

.. code-block:: python

   GET /expressions/search
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "Input payload validation failed"
   }

* **Success Criteria:** :code:`Status Code == 4xx` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 4xx` AND response body is NOT valid :code:`Error` json

Expression Search Filetypes Match
####################################
* **Route:** :code:`/expressions/search`
* **Description:** Search for all expressions, only specifying the required :code:`format` parameter. Checks that all :code:`Expressions` in the response array have a :code:`fileType` that matches the requested :code:`format`.
* **Rationale:** Asserts that the :code:`/expressions/<id>` endpoint does not return arbitrary :code:`Expressions`, only :code:`Expressions` with a :code:`fileType` matching the requested :code:`format`.

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "tags": [],
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "url": "/path/to/E-MTAB-5423-query-results.tpms.loom",
       "units": "TPM",
       "version": "1.0",
       "fileType": "loom"
     },
     {
       "tags": [
         "RNAgetCompliance"
       ],
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/expression.loom",
       "units": "TPM",
       "version": "1.0",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND ALL :code:`Expressions` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR ANY :code:`Expression` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Expression Search No Filetype Mismatches
#########################################
* **Route:** :code:`/expressions/search`
* **Description:** Search for all expressions, only specifying the required :code:`format` parameter. However, the value of :code:`format` is different from that of the test expression file. Checks that all :code:`Expressions` in the response array have a :code:`fileType` that matches the requested :code:`format`.
* **Rationale:** This test is used in conjunction with the above to ensure that only :code:`Expressions` of the correct :code:`fileType` are returned. Asserts that all :code:`Expressions` returned from the above test case are excluded from the response of this test case

* **Request:**

.. code-block:: python

   GET /expressions/search?format=tsv
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND ALL :code:`Expressions` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR ANY :code:`Expression` DOES NOT have a :code:`fileType` matching the requested :code:`format`


Expression API Non-Implemented Test Cases
------------------------------------------

* `Expression Get Not Implemented`_
* `Expression Search Not Implemented`_
* `Expression Search Filters Not Implemented`_
* `Expression Formats Not Implemented`_

Expression Get Not Implemented
###############################
* **Route:** :code:`/expressions/<id>`
* **Description:** If the :code:`Expressions` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/expressions/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /expressions/nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Expression Search Not Implemented
##################################
* **Route:** :code:`/expressions/search`
* **Description:** If the :code:`Expressions` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/expressions/search` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /expressions/search
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Expression Search Filters Not Implemented
##########################################
* **Route:** :code:`/expressions/search/filters`
* **Description:** If the :code:`Expressions` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/expressions/search/filters` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented according to the spec

* **Request:**

.. code-block:: python

   GET /expressions/search/filters
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Expression Formats Not Implemented
##########################################
* **Route:** :code:`/expressions/formats`
* **Description:** If the :code:`Expressions` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/expressions/formats` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented according to the spec

* **Request:**

.. code-block:: python

   GET /expressions/formats
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Expression Content Tests
------------------------

Expression content tests assert that expression matrices downloaded from the 
RNAget server contain the expected content/results based on the request. Matrix
rows, columns, and values are cross-referenced against the request to ensure the
correct data has been returned.

Expression Content Test Cases
------------------------------

* `Expression Get Content`_
* `Expression Search, Slice by featureIDList`_
* `Expression Search, Slice by featureNameList`_
* `Expression Search, Slice by sampleIDList`_
* `Expression Search, Slice by minExpression`_
* `Expression Search, Slice by maxExpression`_
* `Expression Search, Slice by featureIDList and sampleIDList`_
* `Expression Search, Slice by featureNameList and sampleIDList`_
* `Expression Search, Slice by featureIDList, sampleIDList, and minExpression`_
* `Expression Search, Slice by featureIDList, sampleIDList, and maxExpression`_
* `Expression Search, Slice by featureIDList, sampleIDList, minExpression, and maxExpression`_

Expression Get Content
#######################
* **Route:** :code:`/expressions/<id>`
* **Description:** Download test expression, check matrix rows, columns, and expression values against known values
* **Rationale:** Asserts the correct matrix file is associated with the test :code:`Expression`

* **Request:**

.. code-block:: python

   GET /expressions/ac3e9279efd02f1c98de4ed3d335b98e
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Test expression matrix, rows, and values match expected
* **Failure Criteria:** Test expression matrix, rows, and values DO NOT match expected

Expression Search, Slice by featureIDList
##############################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by featureIDList, check that only requested features/genes are in downloaded matrix
* **Rationale:** Asserts search endpoint correctly subsets expression matrix by featureIDList

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&featureIDList=ENSG00000037965,ENSG00000243503,ENSG00000259285
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix contains ONLY genes (rows) requested in featureIDList
* **Failure Criteria:** Downloaded matrix DOES NOT contain ONLY genes (rows) requested in featureIDList

Expression Search, Slice by featureNameList
##############################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by featureNameList, check that only requested features/genes are in downloaded matrix
* **Rationale:** Asserts search endpoint correctly subsets expression matrix by featureNameList

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&featureNameList=PGLYRP3,PRSS50,SNRPFP1,OR5AC4P,CLIC1,RF00092,AC100827.4
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix contains ONLY genes (rows) requested in featureNameList
* **Failure Criteria:** Downloaded matrix DOES NOT contain ONLY genes (rows) requested in featureNameList

Expression Search, Slice by sampleIDList
##############################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by sampleIDList, check that only requested samples (columns) are in downloaded matrix
* **Rationale:** Asserts search endpoint correctly subsets expression matrix by sampleIDList

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&sampleIDList=DO22935 - primary tumour,DO20604 - primary tumour,DO48516 - primary tumour,DO42881 - primary tumour,DO6144 - primary tumour,DO40948 - primary tumour,DO472 - primary tumour,DO48505 - primary tumour
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix contains ONLY samples (columns) requested in sampleIDList
* **Failure Criteria:** Downloaded matrix DOES NOT contain ONLY samples (columns) requested in sampleIDList

Expression Search, Slice by minExpression
##############################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by minExpression, check that all expression values are above minExpression thresholds for each gene
* **Rationale:** Asserts search endpoint correctly subsets expression matrix by minExpression

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&minExpression=[{"threshold": 100,"featureName": "CLIC1"},{"threshold": 50,"featureName": "TSPAN6"},{"threshold": 30,"featureName": "LTV1"}]
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix expression values are above minExpression thresholds for each gene
* **Failure Criteria:** Downloaded matrix expression values are NOT above minExpression thresholds for each gene

Expression Search, Slice by maxExpression
##############################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by maxExpression, check that all expression values are below maxExpression thresholds for each gene
* **Rationale:** Asserts search endpoint correctly subsets expression matrix by maxExpression

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&maxExpression=[{"threshold": 500,"featureName": "CLIC1"},{"threshold": 80,"featureName": "TSPAN6"},{"threshold": 50,"featureName": "LTV1"},{"threshold": 50,"featureName": "TRIM22"},{"threshold": 50,"featureName": "NCOA5"}]
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix expression values are below maxExpression thresholds for each gene
* **Failure Criteria:** Downloaded matrix expression values are NOT below maxExpression thresholds for each gene

Expression Search, Slice by featureIDList and sampleIDList
#############################################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by featureIDList and sampleIDList, check returned rows/columns are an intersection of all filters
* **Rationale:** Asserts search endpoint correctly subsets expression matrix by featureIDList and sampleIDList

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&featureIDList=ENSG00000106278,ENSG00000142025,ENSG00000171487,ENSG00000184471,ENSG00000213719,ENSG00000239589&sampleIDList=DO52655 - primary tumour,DO52685 - primary tumour,DO25887 - primary tumour
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix contains only genes from featureIDList AND samples from sampleIDList
* **Failure Criteria:** Downloaded matrix DOES NOT contain only genes from featureIDList OR samples from sampleIDList

Expression Search, Slice by featureNameList and sampleIDList
##############################################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by featureNameList and sampleIDList, check returned rows/columns are an intersection of all filters
* **Rationale:** Asserts search endpoint correctly subsets expression matrix by featureNameList and sampleIDList

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&featureNameList=SH3BP1,APOL5,RN7SL592P&sampleIDList=DO1249 - primary tumour,DO28763 - primary tumour,DO33408 - primary tumour,DO219961 - primary tumour,DO2995 - primary tumour,DO18671 - primary tumour,DO219106 - primary tumour
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix contains only genes from featureNameList AND samples from sampleIDList
* **Failure Criteria:** Downloaded matrix DOES NOT contain only genes from featureNameList OR samples from sampleIDList

Expression Search, Slice by featureIDList, sampleIDList, and minExpression
############################################################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by featureIDList, sampleIDList, and minExpression, check that only requested genes and samples are in downloaded matrix AND expression values are above minExpression thresholds for each gene
* **Rationale:** Asserts search endpoint correctly subsets expression matrix featureNameList, sampleIDList, and minExpression

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&featureIDList=ENSG00000110876,ENSG00000145740,ENSG00000106278,ENSG00000186501,ENSG00000198677,ENSG00000124160,ENSG00000132274,ENSG00000135521,ENSG00000000003,ENSG00000213719&sampleIDList=DO472 - primary tumour,DO1954 - primary tumour,DO2503 - primary tumour,DO220478 - normal,DO219106 - primary tumour,DO37259 - primary tumour,DO9042 - primary tumour,DO40948 - primary tumour,DO42881 - primary tumour,DO43811 - primary tumour&minExpression=[{"threshold": 400,"featureName": "CLIC1"},{"threshold": 140,"featureName": "TSPAN6"},{"threshold": 35,"featureName": "LTV1"}]
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix contains ONLY genes from featureNameList AND samples from sampleIDList AND values are above minExpression thresholds for each gene
* **Failure Criteria:** Downloaded matrix DOES NOT contain ONLY genes from featureNameList OR samples from sampleIDList OR values are NOT above minExpression thresholds for each gene

Expression Search, Slice by featureIDList, sampleIDList, and maxExpression
############################################################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by featureIDList, sampleIDList, and maxExpression, check that only requested genes and samples are in downloaded matrix AND expression values are below maxExpression thresholds for each gene
* **Rationale:** Asserts search endpoint correctly subsets expression matrix featureNameList, sampleIDList, and maxExpression

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&featureIDList=ENSG00000110876,ENSG00000145740,ENSG00000106278,ENSG00000186501,ENSG00000198677,ENSG00000124160,ENSG00000132274,ENSG00000135521,ENSG00000000003,ENSG00000213719&sampleIDList=DO45161 - primary tumour,DO45217 - primary tumour,DO28763 - primary tumour,DO46342 - primary tumour,DO46366 - primary tumour,DO46380 - primary tumour,DO46408 - primary tumour,DO46556 - recurrent tumour,DO46597 - primary tumour,DO34608 - primary tumour&maxExpression=[{"threshold": 1500,"featureName": "CLIC1"},{"threshold": 450,"featureName": "TSPAN6"},{"threshold": 300,"featureName": "LTV1"}]
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix contains ONLY genes from featureNameList AND samples from sampleIDList AND values are below maxExpression thresholds for each gene
* **Failure Criteria:** Downloaded matrix DOES NOT contain ONLY genes from featureNameList OR samples from sampleIDList OR values are NOT below maxExpression thresholds for each gene

Expression Search, Slice by featureIDList, sampleIDList, minExpression, and maxExpression
############################################################################################
* **Route:** :code:`/expressions/search`
* **Description:** Subset test expression matrix by featureIDList, sampleIDList, minExpression, maxExpression, check that only requested genes and samples are in downloaded matrix AND expression values are above minExpression thresholds for each gene AND expression values are below maxExpression thresholds for each gene
* **Rationale:** Asserts search endpoint correctly subsets expression matrix featureNameList, sampleIDList, minExpression, and maxExpression

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&featureIDList=ENSG00000110876,ENSG00000145740,ENSG00000106278,ENSG00000186501,ENSG00000198677,ENSG00000124160,ENSG00000132274,ENSG00000135521,ENSG00000000003,ENSG00000213719&sampleIDList=DO45161 - primary tumour,DO45217 - primary tumour,DO28763 - primary tumour,DO46342 - primary tumour,DO46366 - primary tumour,DO46380 - primary tumour,DO46408 - primary tumour,DO46556 - recurrent tumour,DO46597 - primary tumour,DO34608 - primary tumour&minExpression=[{"threshold": 400,"featureName": "CLIC1"},{"threshold": 140,"featureName": "TSPAN6"},{"threshold": 35,"featureName": "LTV1"}]&maxExpression=[{"threshold": 1500,"featureName": "CLIC1"},{"threshold": 450,"featureName": "TSPAN6"},{"threshold": 300,"featureName": "LTV1"}]
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Downloaded matrix contains ONLY genes from featureNameList AND samples from sampleIDList AND values are above minExpression thresholds for each gene AND values are below maxExpression thresholds for each gene
* **Failure Criteria:** Downloaded matrix DOES NOT contain ONLY genes from featureNameList OR samples from sampleIDList OR values are NOT above minExpression thresholds for each gene OR values are NOT below maxExpression thresholds for each gene

