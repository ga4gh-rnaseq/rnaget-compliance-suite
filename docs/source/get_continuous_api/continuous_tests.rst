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

* `Get Test Continuous`_
* `Continuous Not Found`_
* `Continuous Get Start Specified Without Chr`_
* `Continuous Get End Specified Without Chr`_
* `Continuous Get Start Greater Than End`_
* `Get Supported Continuous Formats`_
* `Continuous Search Filters`_
* `Search Continuous by Format`_
* `Search Continuous With All Filters`_
* `Search Continuous With Single Filter, 1`_
* `Search Continuous With Single Filter, 2`_
* `Continuous Search Filters Non-Matching Resources`_
* `Continuous Search Format Not Specified`_
* `Continuous Search Filetypes Match`_
* `Continuous Search No Filetype Mismatches`_
* `Continuous Search Start Specified Without Chr`_
* `Continuous Search End Specified Without Chr`_
* `Continuous Search Start Greater Than End`_

Get Test Continuous
####################
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests continuous data by its :code:`id`. Expects signal intensity to be returned as a file attachment.
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint returns a signal intensity file as an attachment.

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.loom
   Content-Disposition: attachment

* **Success Criteria:** :code:`Status Code == 200` AND :code:`Content-Type` corresponds to the file :code:`format` (loom, tsv, etc.)
* **Failure Criteria:** :code:`Status Code != 200` OR :code:`Content-Type` DOES NOT correspond to the file :code:`format` (loom, tsv, etc.)

Continuous Not Found
######################
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests a continuous with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Continuous` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint does not return arbitrary :code:`Continuous` objects, and only returns a :code:`Continuous` when the :code:`id` matches.

* **Request:**

.. code-block:: python

   GET /continuous/nonexistentid9999999999999999999
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 404 Not Found
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "Entry not found in database."
   }

* **Success Criteria:** :code:`Status Code == 404` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 404` OR response body is NOT valid :code:`Error` json

Continuous Get Start Specified Without Chr
###########################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests test continuous by its id, specifying a start position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint raises an error when :code:`start` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?start=5
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous Get End Specified Without Chr
###########################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests test continuous by its id, specifying an end position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint raises an error when :code:`end` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?end=1000
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "chr required if either start or end is specified"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Continuous Get Start Greater Than End
###########################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests test continuous by its id, specifying :code:`chr`, :code:`start`, and :code:`end`, however, :code:`start` position is greater than :code:`end`. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint raises an error when :code:`start` is greater than :code:`end`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=1&start=200&end=100
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 400 Bad Request
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "start cannot be greater than end"
   }

* **Success Criteria:** :code:`Status Code == 400` AND response body is valid :code:`Error` json
* **Failure Criteria:** :code:`Status Code != 400` OR response body is NOT valid :code:`Error` json

Get Supported Continuous Formats
#################################
* **Route:** :code:`/continuous/formats`
* **Description:** Requests the available continuous data file formats on the server. Expects an array of strings to be returned in the response body.
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

Continuous Search Filters
###########################
* **Route:** :code:`/continuous/search/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Continuous`
* **Rationale:** Asserts that the endpoint returns an array of :code:`Search Filter` objects

* **Request:**

.. code-block:: python

   GET /continuous/search/filters
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

Search Continuous by Format
################################
* **Route:** :code:`/continuous/search`
* **Description:** Searches for all continuous, specifying only the required 'format' parameter. Expects an array of :code:`Continuous` in the response body.
* **Rationale:** Asserts that the :code:`/continuous/search` returns an array, and that each element in the array is a :code:`Continuous`.

* **Request:**

.. code-block:: python

   GET /continuous/search?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "fa057c6d18c44960a1b8b49d065b3889",
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "url": "/path/to/signal-query-results.loom",
       "version": "1.0",
       "tags": [
         "cancer"
       ],
       "fileType": "loom"
     },
     {
       "id": "5e22e009f41fc53cbea094a41de8798f",
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/continuous.loom",
       "version": "1.0",
       "tags": [
         "RNAgetCompliance"
       ],
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR :code:`Array Length < 1`

Search Continuous With All Filters
####################################
* **Route:** :code:`/continuous/search`
* **Description:** Searches continuous, using all filtering parameters associated with test continuous. Expects an array of :code:`Continuous` to be returned in the response body. Array must contain at least 1 object.
* **Rationale:** Asserts that :code:`/continuous/search` returns an array of :code:`Continuous` even when specifying filters. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the test continuous.

* **Request:**

.. code-block:: python

   GET /continuous/search?format=loom&version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "5e22e009f41fc53cbea094a41de8798f",
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/continuous.loom",
       "version": "1.0",
       "tags": [
         "RNAgetCompliance"
       ],
       "fileType": "loom"
    }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR :code:`Array Length < 1`

Search Continuous With Single Filter, 1
#########################################
* **Route:** :code:`/continuous/search`
* **Description:** Searches continuous using only 1 filtering parameter associated with test continuous (in addition to format). Expects an array of :code:`Continuous`, with length of 1 or greater.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields the test :code:`Continuous` in the search results.

* **Requests:**

.. code-block:: python

   GET /continuous/search?format=loom&version=1.0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "fa057c6d18c44960a1b8b49d065b3889",
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "url": "/path/to/signal-query-results.loom",
       "version": "1.0",
       "tags": [
         "cancer"
       ],
       "fileType": "loom"
     },
     {
       "id": "5e22e009f41fc53cbea094a41de8798f",
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/continuous.loom",
       "version": "1.0",
       "tags": [
         "RNAgetCompliance"
       ],
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR :code:`Array Length < 1`

Search Continuous With Single Filter, 2
#########################################
* **Route:** :code:`/continuous/search`
* **Description:** Searches continuous using only 1 filtering parameter (a different filter than above) associated with test continuous (in addition to format). Expects an array of :code:`Continuous`, with length of 1 or greater.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields the test :code:`Continuous` in the search results.

* **Requests:**

.. code-block:: python

   GET /continuous/search?format=loom&studyID=f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "5e22e009f41fc53cbea094a41de8798f",
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/path/to/continuous.loom",
       "version": "1.0",
       "tags": [
         "RNAgetCompliance"
       ],
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR :code:`Array Length < 1`

Continuous Search Filters Non-Matching Resources
#################################################
* **Route:** :code:`/continuous/search`
* **Description:** Tests that the continuous search endpoint correctly filters out non-matching :code:`Continuous` based on URL parameters. Makes a request to the :code:`/continuous/search` endpoint with invalid filters (not matching any :code:`Continuous`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Continuous` that differ from filters.

* **Request:**

.. code-block:: python

   GET /continuous/search?format=nonexistentid9999999999999999999&version=nonexistentid9999999999999999999&studyID=nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT an empty array

Continuous Search Format Not Specified
#######################################
* **Route:** :code:`/continuous/search`
* **Description:** Searches for all continuous WITHOUT specifying the required :code:`format` parameter. Expects a :code:`4xx` error response, with an error message indicating that the request was invalid.
* **Rationale:** As the :code:`format` parameter is required to specify file format for the :code:`/continuous/search` endpoint, this test asserts malformed requests raise an error.

* **Request:**

.. code-block:: python

   GET /continuous/search
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

Continuous Search Filetypes Match
####################################
* **Route:** :code:`/continuous/search`
* **Description:** Search for all continuous, only specifying the required :code:`format` parameter. Checks that all :code:`Continuous` in the response array have a :code:`fileType` that matches the requested :code:`format`.
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint does not return arbitrary :code:`Continuous`, only :code:`Continuous` with a :code:`fileType` matching the requested :code:`format`.

* **Request:**

.. code-block:: python

   GET /continuous/search?format=loom
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "fa057c6d18c44960a1b8b49d065b3889",
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "url": "/woldlab/castor/home/sau/public_html/rnaget/signal-query-results.loom",
       "version": "1.0",
       "tags": [
         "cancer"
       ],
       "fileType": "loom"
     },
     {
       "id": "5e22e009f41fc53cbea094a41de8798f",
       "studyID": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "url": "/woldlab/castor/home/sau/public_html/rnaget/continuous.loom",
       "version": "1.0",
       "tags": [
         "RNAgetCompliance"
       ],
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND ALL :code:`Continuous` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR ANY :code:`Continuous` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Continuous Search No Filetype Mismatches
#########################################
* **Route:** :code:`/continuous/search`
* **Description:** Search for all continuous, only specifying the required :code:`format` parameter. However, the value of :code:`format` is different from that of the test continuous file. Checks that all :code:`Continuous` in the response array have a :code:`fileType` that matches the requested :code:`format`.
* **Rationale:** This test is used in conjunction with the above to ensure that only :code:`Continuous` of the correct :code:`fileType` are returned. Asserts that all :code:`Continuous` returned from the above test case are excluded from the response of this test case

* **Request:**

.. code-block:: python

   GET /continuous/search?format=tsv
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND ALL :code:`Continuous` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR ANY :code:`Continuous` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Continuous Search Start Specified Without Chr
##############################################
* **Route:** :code:`/continuous/search`
* **Description:** Search continuous, specifying a start position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/search` endpoint raises an error when :code:`start` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/search?format=loom&start=5
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

Continuous Search End Specified Without Chr
############################################
* **Route:** :code:`/continuous/search`
* **Description:** Search continuous, specifying an end position without a chromosome. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/search` endpoint raises an error when :code:`end` is specified without :code:`chr`

* **Request:**

.. code-block:: python

   GET /continuous/search?format=loom&end=1000
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

Continuous Search Start Greater Than End
###########################################
* **Route:** :code:`/continuous/search`
* **Description:** Search continuous, specifying :code:`chr`, :code:`start`, and :code:`end`, however, :code:`start` position is greater than :code:`end`. Expects a :code:`400 Bad Request` status code in the response, and an error message
* **Rationale:** Asserts that the :code:`/continuous/search` endpoint raises an error when :code:`start` is greater than :code:`end`

* **Request:**

.. code-block:: python

   GET /continuous/search?format=loom&chr=1&start=200&end=100
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

Continuous API Non-Implemented Test Cases
------------------------------------------

* `Continuous Get Not Implemented`_
* `Continuous Search Not Implemented`_
* `Continuous Search Filters Not Implemented`_
* `Continuous Formats Not Implemented`_

Continuous Get Not Implemented
###############################
* **Route:** :code:`/continuous/<id>`
* **Description:** If the :code:`Continuous` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/continuous/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /continuous/nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Search Not Implemented
##################################
* **Route:** :code:`/continuous/search`
* **Description:** If the :code:`Continuous` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/continuous/search` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /continuous/search
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Search Filters Not Implemented
##########################################
* **Route:** :code:`/continuous/search/filters`
* **Description:** If the :code:`Continuous` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/continuous/search/filters` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented according to the spec

* **Request:**

.. code-block:: python

   GET /continuous/search/filters
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Continuous Formats Not Implemented
##########################################
* **Route:** :code:`/continuous/formats`
* **Description:** If the :code:`Continuous` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/continuous/formats` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented according to the spec

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

Continuous Content Tests
-------------------------

Continuous content tests assert that continuous data files/matrices downloaded
from the RNAget server contain the expected content based on the request. 
Continuous file tracks, positions, and intensity values are cross-referenced
against the request to ensure the expected data has been returned.

Continuous Content Test Cases
------------------------------

* `Continuous Get Content, Assert Correct Values, 1`_
* `Continuous Get Content, chr, 1`_
* `Continuous Get Content, chr, 2`_
* `Continuous Get Content, chr and start, 1`_
* `Continuous Get Content, chr and start, 2`_
* `Continuous Get Content, chr and end, 1`_
* `Continuous Get Content, chr and end, 2`_
* `Continuous Get Content, chr, start, and end, 1`_
* `Continuous Get Content, chr, start, and end, 2`_
* `Continuous Search Content, chr, 1`_
* `Continuous Search Content, chr, 2`_
* `Continuous Search Content, chr and start, 1`_
* `Continuous Search Content, chr and start, 2`_
* `Continuous Search Content, chr and end, 1`_
* `Continuous Search Content, chr and end, 2`_
* `Continuous Search Content, chr, start, and end, 1`_
* `Continuous Search Content, chr, start, and end, 2`_

Continuous Get Content, Assert Correct Values, 1
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Download test continuous, check matrix tracks (rows), positions (columns), and signal intensity values against known values
* **Rationale:** Asserts the correct matrix file is associated with the test :code:`Continuous`

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Test continuous matrix, rows, and values match expected
* **Failure Criteria:** Test continuous matrix, rows, and values DO NOT match expected

Continuous Get Content, chr, 1
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Subset test continuous by chr, check matrix only contains positions from requested chr
* **Rationale:** Asserts continuous get endpoint correctly subsets continuous matrix by chr

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=chr1
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr

Continuous Get Content, chr, 2
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Subset test continuous by chr, check matrix only contains positions from requested chr
* **Rationale:** Asserts continuous get endpoint correctly subsets continuous matrix by chr

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=chr5
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr

Continuous Get Content, chr and start, 1
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Subset test continuous by chr and start, check matrix ONLY contains positions from requested chr above or equal to start base
* **Rationale:** Asserts continuous get endpoint correctly subsets continuous matrix by chr and start

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=chr1&start=32
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr above or equal to start base
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr above or equal to start base

Continuous Get Content, chr and start, 2
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Subset test continuous by chr and start, check matrix ONLY contains positions from requested chr above or equal to start base
* **Rationale:** Asserts continuous get endpoint correctly subsets continuous matrix by chr and start

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=chr5&start=100
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr above or equal to start base
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr above or equal to start base

Continuous Get Content, chr and end, 1
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Subset test continuous by chr and end, check matrix ONLY contains positions from requested chr below end base
* **Rationale:** Asserts continuous get endpoint correctly subsets continuous matrix by chr and end

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=chr1&end=22
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr below end base
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr below end base

Continuous Get Content, chr and end, 2
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Subset test continuous by chr and end, check matrix ONLY contains positions from requested chr below end base
* **Rationale:** Asserts continuous get endpoint correctly subsets continuous matrix by chr and end

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=chr5&end=49
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr below end base
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr below end base

Continuous Get Content, chr, start, and end, 1
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Subset test continuous by chr, start, and end, check matrix ONLY contains positions from requested chr between start and end bases
* **Rationale:** Asserts continuous get endpoint correctly subsets continuous matrix by chr, start, and end

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=chr1&start=30&end=50
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr between start and end bases
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr between start and end bases

Continuous Get Content, chr, start, and end, 2
################################################################
* **Route:** :code:`/continuous/<id>`
* **Description:** Subset test continuous by chr, start, and end, check matrix ONLY contains positions from requested chr between start and end bases
* **Rationale:** Asserts continuous get endpoint correctly subsets continuous matrix by chr, start, and end

* **Request:**

.. code-block:: python

   GET /continuous/5e22e009f41fc53cbea094a41de8798f?chr=chr5&start=69&end=117
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr between start and end bases
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr between start and end bases

Continuous Search Content, chr, 1
################################################################
* **Route:** :code:`/continuous/search`
* **Description:** Subset test continuous by chr, check matrix only contains positions from requested chr
* **Rationale:** Asserts continuous search endpoint correctly subsets continuous matrix by chr

* **Request:**

.. code-block:: python

   GET /continuous/search?version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&chr=chr1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr

Continuous Search Content, chr, 2
################################################################
* **Route:** :code:`/continuous/search`
* **Description:** Subset test continuous by chr, check matrix only contains positions from requested chr
* **Rationale:** Asserts continuous search endpoint correctly subsets continuous matrix by chr

* **Request:**

.. code-block:: python

   GET /continuous/search?version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&chr=chr5
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr

Continuous Search Content, chr and start, 1
################################################################
* **Route:** :code:`/continuous/search`
* **Description:** Subset test continuous by chr and start, check matrix ONLY contains positions from requested chr above or equal to start base
* **Rationale:** Asserts continuous search endpoint correctly subsets continuous matrix by chr and start

* **Request:**

.. code-block:: python

   GET /continuous/search?version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&chr=chr1&start=55
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr above or equal to start base
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr above or equal to start base

Continuous Search Content, chr and start, 2
################################################################
* **Route:** :code:`/continuous/search`
* **Description:** Subset test continuous by chr and start, check matrix ONLY contains positions from requested chr above or equal to start base
* **Rationale:** Asserts continuous search endpoint correctly subsets continuous matrix by chr and start

* **Request:**

.. code-block:: python

   GET /continuous/search?version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&chr=chr5&start=16
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr above or equal to start base
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr above or equal to start base

Continuous Search Content, chr and end, 1
################################################################
* **Route:** :code:`/continuous/search`
* **Description:** Subset test continuous by chr and end, check matrix ONLY contains positions from requested chr below end base
* **Rationale:** Asserts continuous search endpoint correctly subsets continuous matrix by chr and end

* **Request:**

.. code-block:: python

   GET /continuous/search?version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&chr=chr1&end=41
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr below end base
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr below end base

Continuous Search Content, chr and end, 2
################################################################
* **Route:** :code:`/continuous/search`
* **Description:** Subset test continuous by chr and end, check matrix ONLY contains positions from requested chr below end base
* **Rationale:** Asserts continuous search endpoint correctly subsets continuous matrix by chr and end

* **Request:**

.. code-block:: python

   GET /continuous/search?version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&chr=chr5&end=73
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr below end base
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr below end base

Continuous Search Content, chr, start, and end, 1
################################################################
* **Route:** :code:`/continuous/search`
* **Description:** Subset test continuous by chr, start, and end, check matrix ONLY contains positions from requested chr between start and end bases
* **Rationale:** Asserts continuous search endpoint correctly subsets continuous matrix by chr, start, and end

* **Request:**

.. code-block:: python

   GET /continuous/search?version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&chr=chr1&start=51&end=66
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr between start and end bases
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr between start and end bases

Continuous Search Content, chr, start, and end, 2
################################################################
* **Route:** :code:`/continuous/search`
* **Description:** Subset test continuous by chr, start, and end, check matrix ONLY contains positions from requested chr between start and end bases
* **Rationale:** Asserts continuous search endpoint correctly subsets continuous matrix by chr, start, and end

* **Request:**

.. code-block:: python

   GET /continuous/search?version=1.0&studyID=f3ba0b59bed0fa2f1030e7cb508324d1&chr=chr5&start=102&end=115
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Success Criteria:** Matrix contains ONLY positions from request chr between start and end bases
* **Failure Criteria:** Matrix DOES NOT contain ONLY positions from request chr between start and end bases
