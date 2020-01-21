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

* `Get Supported Expression Formats`_
* `Expression Filters`_
* `Get Test Expression Ticket`_
* `Single Expression Ticket - Not Found`_
* `Get Test Expression Bytes`_
* `Single Expression Bytes - Not Found`_
* `Expression Ticket by Format`_
* `Expression Ticket - All Filters`_
* `Expression Ticket - Single Filter, 1`_
* `Expression Ticket - Single Filter, 2`_
* `Expression Ticket - Format Not Specified`_
* `Expression Ticket - Filetype Matches`_
* `Expression Bytes by Format`_
* `Expression Bytes - All Filters`_
* `Expression Bytes - Single Filter, 1`_
* `Expression Bytes - Single Filter, 2`_
* `Expression Bytes - Format Not Specified`_

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

Expression Filters
###########################
* **Route:** :code:`/expressions/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Expressions`
* **Rationale:** Asserts that the endpoint returns an array of :code:`filter` objects

* **Request:**

.. code-block:: python

   GET /expressions/filters
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

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`filters`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`filters`

Get Test Expression Ticket
############################
* **Route:** :code:`/expressions/<id>/ticket`
* **Description:** Requests test expression :code:`ticket` by its :code:`id`. Expects the returned expression to match the :code:`ticket` json schema.
* **Rationale:** Asserts that the :code:`/expressions/<id>/ticket` endpoint returns a valid :code:`ticket`.

* **Request:**

.. code-block:: python

   GET /expressions/ac3e9279efd02f1c98de4ed3d335b98e/ticket
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
     "units": "TPM",
     "fileType": "loom/tsv"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is valid :code:`ticket`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT valid :code:`ticket`

Single Expression Ticket - Not Found
######################################
* **Route:** :code:`/expressions/<id>/ticket`
* **Description:** Requests an expression ticket with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Expression` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with an error message.
* **Rationale:** Asserts that the :code:`/expressions/<id>/ticket` endpoint does not return arbitrary :code:`ticket`.

* **Request:**

.. code-block:: python

   GET /expressions/nonexistentid9999999999999999999/ticket
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

Get Test Expression Bytes
##########################
* **Route:** :code:`/expressions/<id>/bytes`
* **Description:** Requests test expression matrix as :code:`bytes` by its :code:`id`.
* **Rationale:** Asserts that the :code:`/expressions/<id>/bytes` endpoint returns matrix bytes.

* **Request:**

.. code-block:: python

   GET /expressions/ac3e9279efd02f1c98de4ed3d335b98e/bytes
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Single Expression Bytes - Not Found
####################################
* **Route:** :code:`/expressions/<id>/bytes`
* **Description:** Requests expression matrix :code:`bytes` with an invalid :code:`id` that doesn't correspond to any :code:`Expression` on the server. Expects a :code:`404 Not Found` status code and an error message in response body.
* **Rationale:** Asserts that the :code:`/expressions/<id>/bytes` endpoint does not return arbitrary matrix.

* **Request:**

.. code-block:: python

   GET /expressions/nonexistentid9999999999999999999/bytes
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 404 Not Found
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "Entry not found in database."
   }

* **Success Criteria:** :code:`Status Code == 404` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 404` OR response body is NOT valid :code:`Error` json

Expression Ticket by Format
################################
* **Route:** :code:`/expressions/ticket`
* **Description:** Requests joined matrix, specifying only the required 'format' parameter. Expects :code:`ticket` response.
* **Rationale:** Asserts that the :code:`/expressions/ticket` returns a valid :code:`ticket`.

* **Request:**

.. code-block:: python

   GET /expressions/ticket?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

    {
      "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
      "url": "/path/to/E-MTAB-5423-query-results.tpms.loom",
      "units": "TPM",
      "version": "1.0",
      "fileType": "loom"
    }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket`

Expression Ticket - All Filters
####################################
* **Route:** :code:`/expressions/ticket`
* **Description:** Requests joined matrix, using all filtering parameters associated with test expression. Expects :code:`ticket`.
* **Rationale:** Asserts that :code:`/expressions/ticket` returns :code:`ticket` when specifying filters.

* **Request:**

.. code-block:: python

   GET /expressions/ticket?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

    {
      "url": "https://path/to/expression.loom",
      "units": "TPM",
      "fileType": "loom"
    }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket`

Expression Ticket - Single Filter, 1
#########################################
* **Route:** :code:`/expressions/ticket`
* **Description:** Requests joined matrix using only 1 filtering parameter associated with test expression (in addition to format). Expects :code:`ticket`.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields a valid :code:`ticket`.

* **Requests:**

.. code-block:: python

   GET /expressions/ticket?format=loom&version=1.0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

    {
      "url": "https://path/to/expression.loom",
      "units": "TPM",
      "version": "1.0",
      "fileType": "loom"
    }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket`

Expression Ticket - Single Filter, 2
#########################################
* **Route:** :code:`/expressions/ticket`
* **Description:** Requests joined matrix using only 1 filtering parameter (a different filter than above) associated with test expression (in addition to format). Expects :code:`ticket`.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields a valid :code:`ticket`.

* **Requests:**

.. code-block:: python

   GET /expressions/ticket?format=loom&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

    {
      "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
      "url": "/path/to/expression.loom",
      "units": "TPM",
      "fileType": "loom"
    }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket`.
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket`.

Expression Ticket - Format Not Specified
##########################################
* **Route:** :code:`/expressions/ticket`
* **Description:** Requests joined matrix WITHOUT specifying the required :code:`format` parameter. Expects a :code:`4xx` response with error message.
* **Rationale:** As the :code:`format` parameter is required to specify file format for the :code:`/expressions/ticket` endpoint, this test asserts malformed requests raise an error.

* **Request:**

.. code-block:: python

   GET /expressions/ticket
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

Expression Ticket - Filetype Matches
######################################
* **Route:** :code:`/expressions/ticket`
* **Description:** Requests joined matrix, only specifying the required :code:`format` parameter. Checks that :code:`ticket` has a :code:`fileType` matching requested :code:`format`.
* **Rationale:** Asserts that the :code:`/expressions/ticket` endpoint returns :code:`ticket` with fileType matching the request.

* **Request:**

.. code-block:: python

   GET /expressions/ticket?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

    {
      "url": "/path/to/E-MTAB-5423-query-results.tpms.loom",
      "units": "TPM",
      "fileType": "loom"
    }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket` AND :code:`fileType` matches requested :code:`format`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket` OR :code:`fileType` DOES NOT match requested :code:`format`

Expression Bytes by Format
############################
* **Route:** :code:`/expressions/bytes`
* **Description:** Requests joined matrix bytes, only specifying the required :code:`format` parameter.
* **Rationale:** Asserts that the :code:`/expressions/bytes` endpoint returns matrix bytes.

* **Request:**

.. code-block:: python

   GET /expressions/bytes?format=loom
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Expression Bytes - All Filters
###############################
* **Route:** :code:`/expressions/bytes`
* **Description:** Requests joined matrix bytes using all expression filters.
* **Rationale:** Asserts that the :code:`/expressions/bytes` endpoint returns matrix bytes when all filters are provided.

* **Request:**

.. code-block:: python

   GET /expressions/bytes?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Expression Bytes - Single Filter, 1
#####################################
* **Route:** :code:`/expressions/bytes`
* **Description:** Requests joined matrix bytes using one expression filter (in addition to format).
* **Rationale:** Asserts filter parameters can be used independently of one another.

* **Request:**

.. code-block:: python

   GET /expressions/bytes?format=loom&version=1.0
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Expression Bytes - Single Filter, 2
####################################
* **Route:** :code:`/expressions/bytes`
* **Description:** Requests joined matrix bytes using one expression filter (different than above), in addition to format.
* **Rationale:** Asserts filter parameters can be used independently of one another.

* **Request:**

.. code-block:: python

   GET /expressions/bytes?format=loom&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream
  
* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Expression Bytes - Format Not Specified
########################################
* **Route:** :code:`/expressions/bytes`
* **Description:** Requests joined matrix bytes WITHOUT specifying required :code:`format` parameter. Expects a :code:`4xx` response with error message.
* **Rationale:** As the :code:`format` parameter is required to specify file format for the :code:`/expressions/bytes` endpoint, this test asserts malformed requests raise an error.

* **Request:**

.. code-block:: python

   GET /expressions/bytes
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "Input payload validation failed"
   }

* **Success Criteria:** :code:`Status Code == 4xx` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 4xx` AND response body is NOT valid :code:`Error` json

Expression API Non-Implemented Test Cases
------------------------------------------

* `Expression Formats Not Implemented`_
* `Expression Ticket by Id Not Implemented`_
* `Expression Bytes by Id Not Implemented`_
* `Expression Filters Not Implemented`_
* `Expression Ticket Not Implemented`_
* `Expression Bytes Not Implemented`_

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

Expression Ticket by Id Not Implemented
#######################################
* **Route:** :code:`/expressions/<id>/ticket`
* **Description:** If expressions endpoints are :code:`Not Implemented`, this test will request :code:`/expressions/<id>/ticket`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts :code:`Expression` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /expressions/nonexistentid9999999999999999999/ticket
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Expression Bytes by Id Not Implemented
########################################

* **Route:** :code:`/expressions/<id>/bytes`
* **Description:** If expressions endpoints are :code:`Not Implemented`, this test will request :code:`/expressions/<id>/bytes`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts :code:`Expression` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /expressions/nonexistentid9999999999999999999/bytes
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Expression Filters Not Implemented
##########################################
* **Route:** :code:`/expressions/filters`
* **Description:** If expressions endpoints are :code:`Not Implemented`, this test will request :code:`/expressions/filters`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /expressions/filters
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Expression Ticket Not Implemented
##################################
* **Route:** :code:`/expressions/ticket`
* **Description:** If expressions endpoints are :code:`Not Implemented`, this test will request :code:`/expressions/ticket`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /expressions/ticket
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Expression Bytes Not Implemented
#################################
* **Route:** :code:`/expressions/bytes`
* **Description:** If expressions endpoints are :code:`Not Implemented`, this test will request :code:`/expressions/bytes`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /expressions/bytes
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

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

* `Expression Ticket by Id Content Test Cases`_
* `Expression Bytes by Id Content Test Cases`_
* `Expression Ticket Content Test Cases`_
* `Expression Bytes Content Test Cases`_

Expression Ticket by Id Content Test Cases
###########################################
* **Route:** :code:`/expressions/<id>/ticket`
* **Description:** Download test expression by ticket multiple times (sometimes slicing by featureIDList, featureNameList, sampleIDList).
* **Rationale:** Asserts correct matrix file is associated with the test expression :code:`id`. Validates expression values match expected. Validates returned columns/rows match expected based on slice parameters.

* **Request:**

.. code-block:: python

   GET /expressions/ac3e9279efd02f1c98de4ed3d335b98e/ticket
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Test expression matrix columns, rows, values match expected
* **Failure Criteria:** Test expression matrix columns, rows, values DO NOT match expected

Expression Bytes by Id Content Test Cases
###########################################
* **Route:** :code:`/expressions/<id>/bytes`
* **Description:** Download test expression by bytes multiple times (sometimes slicing by featureIDList, featureNameList, sampleIDList).
* **Rationale:** Asserts correct matrix file is associated with the test expression :code:`id`. Validates expression values match expected. Validates returned columns/rows match expected based on slice parameters.

* **Request:**

.. code-block:: python

   GET /expressions/ac3e9279efd02f1c98de4ed3d335b98e/bytes
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Test expression matrix columns, rows, values match expected
* **Failure Criteria:** Test expression matrix columns, rows, values DO NOT match expected

Expression Ticket Content Test Cases
###########################################
* **Route:** :code:`/expressions/ticket`
* **Description:** Download joined expression matrix by ticket multiple times (sometimes slicing by featureIDList, featureNameList, sampleIDList).
* **Rationale:** Asserts joined matrix. Validates expression values match expected. Validates returned columns/rows match expected based on slice parameters.

* **Request:**

.. code-block:: python

   GET /expressions/ticket?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Joined expression matrix columns, rows, values match expected
* **Failure Criteria:** Joined expression matrix columns, rows, values DO NOT match expected

Expression Bytes Content Test Cases
###########################################
* **Route:** :code:`/expressions/bytes`
* **Description:** Download joined expression matrix by bytes multiple times (sometimes slicing by featureIDList, featureNameList, sampleIDList).
* **Rationale:** Asserts joined matrix. Validates expression values match expected. Validates returned columns/rows match expected based on slice parameters.

* **Request:**

.. code-block:: python

   GET /expressions/bytes?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Joined expression matrix columns, rows, values match expected
* **Failure Criteria:** Joined expression matrix columns, rows, values DO NOT match expected
