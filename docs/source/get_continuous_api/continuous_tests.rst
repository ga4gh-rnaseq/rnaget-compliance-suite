Continuous Tests
===================

This page outlines the success and failure criteria for all tests of Continuous resources.

Continuous API Tests
---------------------

Continuous API tests assert the correct configuration of continuous-related API 
routes. In order for a test case to succeed, the following conditions must be
met when evaluating the response:
    
    * For all cases, :code:`Content-Type` checking is enforced. For most routes, a value of :code:`application/vnd.ga4gh.rnaget.v1.0.0+json` OR :code:`application/json` is expected. For the :code:`/continuous/<id>` endpoint, a content type matching the format of the file attachment is expected.
    * For all cases, :code:`Status Code` checking is enforced. The response **MUST** have the expected status code
    * For all cases, schema checking is enforced. The json object in the response body **MUST** conform to a pre-defined schema of required fields and data types, which is specific to each API route

Continuous API Test Cases
--------------------------

* `Get Supported Continuous Formats`_
* `Continuous Filters`_
* `Get Test Continuous Ticket`_
* `Single Continuous Ticket - Not Found`_
* `Single Continuous Ticket - Start Specified Without Chr`_
* `Single Continuous Ticket - End Specified Without Chr`_
* `Single Continuous Ticket - Start Greater Than End`_
* `Get Test Continuous Bytes`_
* `Single Continuous Bytes - Not Found`_
* `Single Continuous Bytes - Start Specified Without Chr`_
* `Single Continuous Bytes - End Specified Without Chr`_
* `Single Continuous Bytes - Start Greater Than End`_
* `Continuous Ticket by Format`_
* `Continuous Ticket - All Filters`_
* `Continuous Ticket - Single Filter, 1`_
* `Continuous Ticket - Single Filter, 2`_
* `Continuous Ticket - Format Not Specified`_
* `Continuous Ticket - Filetype Matches`_
* `Continuous Ticket - Start Specified Without Chr`_
* `Continuous Ticket - End Specified Without Chr`_
* `Continuous Ticket - Start Greater Than End`_
* `Continuous Bytes by Format`_
* `Continuous Bytes - All Filters`_
* `Continuous Bytes - Single Filter, 1`_
* `Continuous Bytes - Single Filter, 2`_
* `Continuous Bytes - Format Not Specified`_
* `Continuous Bytes - Start Specified Without Chr`_
* `Continuous Bytes - End Specified Without Chr`_
* `Continuous Bytes - Start Greater Than End`_

Get Supported Continuous Formats
#################################
* **Route:** :code:`/continuous/formats`
* **Description:** Requests the available continuous file formats on the server. Expects an array of strings to be returned in the response body.
* **Rationale:** Asserts that :code:`/continuous/formats` returns an array of strings, indicating which continuous file formats the server supports

* **Request:**

.. code-block:: python

   GET /continuous/formats
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

Continuous Filters
###########################
* **Route:** :code:`/continuous/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Continuous`
* **Rationale:** Asserts that the endpoint returns an array of :code:`filters`

* **Request:**

.. code-block:: python

   GET /continuous/filters
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

Get Test Continuous Ticket
###########################
* **Route:** :code:`/continuous/<id>/ticket`
* **Description:** Requests continuous ticket by its :code:`id`. Expects valid :code:`ticket`.
* **Rationale:** Asserts that :code:`/continuous/<id>/ticket` returns valid :code:`ticket`.

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/ticket
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "id": "5e22e009f41fc53cbea094a41de8798f",
     "version": "1.0",
     "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
     "url": "https://url/to/continuous/file",
     "tags": [
       "RNAgetCompliance"
     ],
     "units": "TPM",
     "fileType": "loom/tsv"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response is :code:`ticket`
* **Failure Criteria:** :code:`Status Code != 200` OR response is NOT :code:`ticket`

Single Continuous Ticket - Not Found
######################################
* **Route:** :code:`/continuous/<id>/ticket`
* **Description:** Requests continuous ticket with an invalid :code:`id`. Expects a :code:`404 Not Found` status code in the response, and error message.
* **Rationale:** Asserts that the :code:`/continuous/<id>/ticket` endpoint does not return arbitrary :code:`ticket`.

* **Request:**

.. code-block:: python

   GET /continuous/nonexistentid9999999999999999999/ticket
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

Single Continuous Ticket - Start Specified Without Chr
########################################################
* **Route:** :code:`/continuous/<id>/ticket`
* **Description:** Requests continuous ticket by its id, specifying a start position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>/ticket` endpoint raises an error when :code:`start` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/ticket?start=5
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Single Continuous Ticket - End Specified Without Chr
#####################################################
* **Route:** :code:`/continuous/<id>/ticket`
* **Description:** Requests test continuous by its id, specifying an end position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>/ticket` endpoint raises an error when :code:`end` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/ticket?end=1000
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Single Continuous Ticket - Start Greater Than End
##################################################
* **Route:** :code:`/continuous/<id>/ticket`
* **Description:** Requests test continuous ticket by its id, specifying :code:`chr`, :code:`start`, and :code:`end`, however, :code:`start` position is greater than :code:`end`. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>/ticket` endpoint raises an error when :code:`start` is greater than :code:`end`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/ticket?chr=1&start=200&end=100
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "start cannot be greater than end"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Get Test Continuous Bytes
##########################
* **Route:** :code:`/continuous/<id>/bytes`
* **Description:** Requests continuous matrix bytes by its :code:`id`.
* **Rationale:** Asserts that :code:`/continuous/<id>/bytes` returns matrix bytes.

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/bytes
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Single Continuous Bytes - Not Found
#####################################

* **Route:** :code:`/continuous/<id>/bytes`
* **Description:** Requests continuous bytes with an invalid :code:`id`. Expects a :code:`404 Not Found` status code in the response, and error message.
* **Rationale:** Asserts that the :code:`/continuous/<id>/bytes` endpoint does not return arbitrary matrix.

* **Request:**

.. code-block:: python

   GET /continuous/nonexistentid9999999999999999999/bytes
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

Single Continuous Bytes - Start Specified Without Chr
#######################################################
* **Route:** :code:`/continuous/<id>/bytes`
* **Description:** Requests continuous matrix bytes by its id, specifying a start position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>/bytes` endpoint raises an error when :code:`start` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/bytes?start=5
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Single Continuous Bytes - End Specified Without Chr
####################################################
* **Route:** :code:`/continuous/<id>/bytes`
* **Description:** Requests test continuous matrix bytes by its id, specifying an end position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>/bytes` endpoint raises an error when :code:`end` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/bytes?end=1000
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Single Continuous Bytes - Start Greater Than End
#################################################
* **Route:** :code:`/continuous/<id>/bytes`
* **Description:** Requests test continuous matrix bytes by its id, specifying :code:`chr`, :code:`start`, and :code:`end`, however, :code:`start` position is greater than :code:`end`. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>/bytes` endpoint raises an error when :code:`start` is greater than :code:`end`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/bytes?chr=1&start=200&end=100
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "start cannot be greater than end"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous Ticket by Format
################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Requests joined continuous matrix, specifying only the required 'format' parameter. Expects :code:`ticket`.
* **Rationale:** Asserts that :code:`/continuous/ticket` returns a :code:`ticket` with which the matrix can be downloaded.

* **Request:**

.. code-block:: python

   GET /continuous/ticket?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
     "url": "/path/to/signal-query-results.loom",
     "units": "TPM",
     "version": "1.0",
     "tags": [
       "cancer"
     ],
     "fileType": "loom"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket`

Continuous Ticket - All Filters
####################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Requests joined continuous matrix, using all filtering parameters. Expects :code:`ticket`.
* **Rationale:** Asserts that :code:`/continuous/ticket` returns :code:`ticket` when specifying filters.

* **Request:**

.. code-block:: python

   GET /continuous/ticket?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
     "url": "/path/to/continuous.loom",
     "units": "TPM",
     "version": "1.0",
     "tags": [
       "RNAgetCompliance"
     ],
     "fileType": "loom"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket`

Continuous Ticket - Single Filter, 1
#########################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Requests joined continuous matrix, using only 1 filtering parameter associated with test continuous (in addition to format). Expects :code:`ticket`.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields a valid :code:`ticket`.

* **Requests:**

.. code-block:: python

   GET /continuous/ticket?format=loom&version=1.0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "url": "/path/to/signal-query-results.loom",
     "units": "TPM",
     "version": "1.0",
     "fileType": "loom"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket`.
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket`.

Continuous Ticket - Single Filter, 2
#########################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Requests joined continuous matrix, using only 1 filtering parameter (different than above) associated with test continuous (in addition to format). Expects :code:`ticket`.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields a valid :code:`ticket`.

* **Requests:**

.. code-block:: python

   GET /continuous/ticket?format=loom&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
     "url": "/path/to/signal-query-results.loom",
     "units": "TPM",
     "fileType": "loom"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket`.
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket`.

Continuous Ticket - Format Not Specified
##########################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Requests joined continuous matrix WITHOUT specifying the required :code:`format` parameter. Expects a :code:`4xx` response with error message.
* **Rationale:** As the :code:`format` parameter is required to specify file format for the :code:`/continuous/ticket` endpoint, this test asserts malformed requests raise an error.

* **Request:**

.. code-block:: python

   GET /continuous/ticket
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

Continuous Ticket - Filetype Matches
####################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Request joined continuous matrix, only specifying the required :code:`format` parameter. Checks that :code:`ticket` has a :code:`fileType` matching requested :code:`format`.
* **Rationale:** Asserts that the :code:`/continuous/ticket` endpoint returns :code:`ticket` with fileType matching the request.

* **Request:**

.. code-block:: python

   GET /continuous/ticket?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
     "url": "/woldlab/castor/home/sau/public_html/rnaget/signal-query-results.loom",
     "units": "TPM",
     "version": "1.0",
     "fileType": "loom"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is :code:`ticket` AND :code:`fileType` matches requested :code:`format`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT :code:`ticket` OR :code:`fileType` DOES NOT match requested :code:`format`

Continuous Ticket - Start Specified Without Chr
################################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Requests joined continuous matrix ticket, specifying a start position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/ticket` endpoint raises an error when :code:`start` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/ticket?format=loom&start=5
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous Ticket - End Specified Without Chr
##############################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Requests joined continuous matrix ticket, specifying an end position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/ticket` endpoint raises an error when :code:`end` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/ticket?format=loom&end=1000
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous Ticket - Start Greater Than End
###########################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Requests joined continuous matrix ticket, specifying :code:`chr`, :code:`start`, and :code:`end`, however, :code:`start` position is greater than :code:`end`. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/ticket` endpoint raises an error when :code:`start` is greater than :code:`end`

* **Request:**

.. code-block:: python

   GET /continuous/ticket?format=loom&chr=1&start=200&end=100
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "start cannot be greater than end"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous Bytes by Format
###############################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Requests joined continuous matrix as bytes, specifying only the required 'format' parameter.
* **Rationale:** Asserts that :code:`/continuous/bytes` returns matrix bytes.

* **Request:**

.. code-block:: python

   GET /continuous/bytes?format=loom
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Continuous Bytes - All Filters
###############################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Requests joined continuous matrix as bytes, using all filtering parameters.
* **Rationale:** Asserts that :code:`/continuous/ticket` returns matrix bytes when specifying filters.

* **Request:**

.. code-block:: python

   GET /continuous/bytes?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Continuous Bytes - Single Filter, 1
###############################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Requests joined continuous matrix as bytes, using only 1 filtering parameter associated with test continuous (in addition to format).
* **Rationale:** Asserts filtering parameters can be used independently of one another.

* **Requests:**

.. code-block:: python

   GET /continuous/bytes?format=loom&version=1.0
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Continuous Bytes - Single Filter, 2
###############################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Requests joined continuous matrix as bytes, using only 1 filtering parameter (different than above) associated with test continuous (in addition to format).
* **Rationale:** Asserts filtering parameters can be used independently of one another.

* **Requests:**

.. code-block:: python

   GET /continuous/bytes?format=loom&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/octet-stream

* **Success Criteria:** :code:`Status Code == 200`
* **Failure Criteria:** :code:`Status Code != 200`

Continuous Bytes - Format Not Specified
###############################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Requests joined continuous matrix as bytes WITHOUT specifying the required :code:`format` parameter. Expects a :code:`4xx` response with error message.
* **Rationale:** As the :code:`format` parameter is required to specify file format for the :code:`/continuous/bytes` endpoint, this test asserts malformed requests raise an error.

* **Request:**

.. code-block:: python

   GET /continuous/bytes
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

Continuous Bytes - Start Specified Without Chr
###############################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Requests joined continuous matrix as bytes, specifying a start position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/bytes` endpoint raises an error when :code:`start` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/bytes?format=loom&start=5
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous Bytes - End Specified Without Chr
###############################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Requests joined continuous matrix as bytes, specifying an end position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/bytes` endpoint raises an error when :code:`end` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/bytes?format=loom&end=1000
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous Bytes - Start Greater Than End
###############################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Requests joined continuous matrix as bytes, specifying :code:`chr`, :code:`start`, and :code:`end`, however, :code:`start` position is greater than :code:`end`. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/bytes` endpoint raises an error when :code:`start` is greater than :code:`end`

* **Request:**

.. code-block:: python

   GET /continuous/bytes?format=loom&chr=1&start=200&end=100
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "start cannot be greater than end"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous API Non-Implemented Test Cases
------------------------------------------

* `Continuous Formats Not Implemented`_
* `Continuous Ticket by Id Not Implemented`_
* `Continuous Bytes by Id Not Implemented`_
* `Continuous Filters Not Implemented`_
* `Continuous Ticket Not Implemented`_
* `Continuous Bytes Not Implemented`_

Continuous Formats Not Implemented
##########################################
* **Route:** :code:`/continuous/formats`
* **Description:** If :code:`Continuous` endpoints are :code:`Not Implemented`, then request :code:`/continuous/formats`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /continuous/formats
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Ticket By Id Not Implemented
#########################################
* **Route:** :code:`/continuous/<id>/ticket`
* **Description:** If :code:`Continuous` endpoints are :code:`Not Implemented`, then request :code:`/continuous/<id>/ticket`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /continuous/nonexistentid9999999999999999999/ticket
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Bytes By Id Not Implemented
#########################################
* **Route:** :code:`/continuous/<id>/bytes`
* **Description:** If :code:`Continuous` endpoints are :code:`Not Implemented`, then request :code:`/continuous/<id>/bytes`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /continuous/nonexistentid9999999999999999999/bytes
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Filters Not Implemented
##########################################
* **Route:** :code:`/continuous/filters`
* **Description:** If :code:`Continuous` endpoints are :code:`Not Implemented`, then request :code:`/continuous/filters`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /continuous/filters
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Ticket Not Implemented
##################################
* **Route:** :code:`/continuous/ticket`
* **Description:** If :code:`Continuous` endpoints are :code:`Not Implemented`, then request :code:`/continuous/ticket`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /continuous/ticket?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Bytes Not Implemented
##################################
* **Route:** :code:`/continuous/bytes`
* **Description:** If :code:`Continuous` endpoints are :code:`Not Implemented`, then request :code:`/continuous/bytes`, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented

* **Request:**

.. code-block:: python

   GET /continuous/bytes?format=loom
   Accept: application/octet-stream, application/vnd.loom, text/tab-separated-values

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Content Tests
-------------------------

Continuous content tests assert that continuous matrices downloaded
from the RNAget server contain the expected content based on the request. 
Continuous file tracks, positions, and intensity values are cross-referenced
against the request to ensure the expected data has been returned.

Continuous Content Test Cases
------------------------------

* `Continuous Ticket by Id Content Test Cases`_
* `Continuous Bytes by Id Content Test Cases`_
* `Continuous Ticket Content Test Cases`_
* `Continuous Bytes Content Test Cases`_

Continuous Ticket by Id Content Test Cases
###########################################
* **Route:** :code:`/continuous/<id>/ticket`
* **Description:** Download test continuous matrix by ticket multiple times (sometimes slicing by chr, start, end).
* **Rationale:** Asserts correct matrix file is associated with the test continuous :code:`id`. Validates signal intensity values match expected. Validates returned columns/rows match expected based on slice parameters.

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/ticket
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Test continuous matrix columns, rows, values match expected
* **Failure Criteria:** Test continuous matrix columns, rows, values DO NOT match expected

Continuous Bytes by Id Content Test Cases
###########################################
* **Route:** :code:`/continuous/<id>/bytes`
* **Description:** Download test continuous matrix bytes multiple times (sometimes slicing by chr, start, end).
* **Rationale:** Asserts correct matrix file is associated with the test continuous :code:`id`. Validates signal intensity values match expected. Validates returned columns/rows match expected based on slice parameters.

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f/bytes
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Test continuous matrix columns, rows, values match expected
* **Failure Criteria:** Test continuous matrix columns, rows, values DO NOT match expected

Continuous Ticket Content Test Cases
###########################################
* **Route:** :code:`/continuous/ticket`
* **Description:** Download joined continuous matrix by ticket multiple times (sometimes slicing by chr, start, end).
* **Rationale:** Asserts joined matrix. Validates signal intensity values match expected. Validates returned columns/rows match expected based on slice parameters.

* **Request:**

.. code-block:: python

   GET /continuous/ticket?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Joined continuous matrix columns, rows, values match expected
* **Failure Criteria:** Joined continuous matrix columns, rows, values DO NOT match expected

Continuous Bytes Content Test Cases
###########################################
* **Route:** :code:`/continuous/bytes`
* **Description:** Download joined continuous matrix as bytes multiple times (sometimes slicing by chr, start, end).
* **Rationale:** Asserts joined matrix. Validates signal intensity values match expected. Validates returned columns/rows match expected based on slice parameters.

* **Request:**

.. code-block:: python

   GET /continuous/bytes?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Joined continuous matrix columns, rows, values match expected
* **Failure Criteria:** Joined continuous matrix columns, rows, values DO NOT match expected
