Continuous Tests
===================

This page outlines the success and failure criteria for all tests of Continuous API routes.

Important Points

* In order for a test to succeed, the following conditions must be met when evaluating the response
    
    * For all tests, :code:`Content-Type` checking is enforced. The response **MUST** have the expected :code:`Content-Type` header. For most routes, a value of :code:`application/vnd.ga4gh.rnaget.v1.0.0+json` OR :code:`application/json` is expected. For the :code:`/continuous/<id>` endpoint, a content type matching the format of the file attachment is expected.
    * For all tests, :code:`Status Code` checking is enforced. The response **MUST** have the expected status code
    * For all tests, schema checking is enforced. The json object in the response body **MUST** conform to a pre-defined schema of required fields and data types, which is specific to each API route

Continuous test cases are discussed below

Continuous Test Cases
----------------------

* `Continuous Get`_
* `Continuous Get Not Found`_
* `Continuous Formats`_
* `Continuous Search`_
* `Continuous Search URL Params All`_
* `Continuous Search URL Params Cases`_
* `Continuous Search Filters Out`_
* `Continuous Search Format Not Specified`_
* `Continuous Search Formats Match`_
* `Continuous Search No Format Mismatches`_
* `Continuous Search Filters`_
* `Continuous Endpoint Not Implemented`_

Continuous Get
###############
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests continuous data by its :code:`id`. Expects signal intensity to be returned as a file attachment.
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint returns a signal intensity file as an attachment.

* **Request:**

.. code-block:: python

   GET /continuous/fa057c6d18c44960a1b8b49d065b3889
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.loom
   Content-Disposition: attachment

* **Success Criteria:** :code:`Status Code == 200` AND :code:`Content-Type` corresponds to the file :code:`format` (loom, tsv, etc.)
* **Failure Criteria:** :code:`Status Code != 200` OR :code:`Content-Type` DOES NOT correspond to the file :code:`format` (loom, tsv, etc.)

Continuous Get Not Found
##########################
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests a continuous with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Continuous` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint does not return arbitrary :code:`Continuous` data, and only returns :code:`Continuous` data when the :code:`id` matches.

* **Request:**

.. code-block:: python

   GET /continuous/999999999999999
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

Continuous Formats
###################
* **Route:** :code:`/continuous/formats`
* **Description:** Requests the available continuous data file formats on the server. Expects an array of strings to be returned in the response body.
* **Rationale:** Asserts that :code:`/continuous/formats` returns an array of strings, indicating which file formats the server supports

* **Request:**

.. code-block:: python

   GET /continuous/formats
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     "loom"
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is an array of strings in json format
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT an array of strings in json format

Continuous Search
##################
* **Route:** :code:`/continuous/search`
* **Description:** Searches for all continuous objects, only specifying the required :code:`format` parameter. Expects an array of :code:`Continuous` objects in the response body.
* **Rationale:** Asserts that the :code:`/continuous/search` returns an array, and that each element in the array is of type :code:`Continuous`.

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
       "tags": [
         "cancer"
       ],
       "URL": "/continuous.loom",
       "id": "fa057c6d18c44960a1b8b49d065b3889",
       "fileType": "loom",
       "version": "1.0",
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR :code:`Array Length < 1`

Continuous Search URL Params All
#################################
* **Route:** :code:`/continuous/search`
* **Description:** Searches continuous objects, using all filtering parameters specified in the config file. Expects an array of :code:`Continuous` objects to be returned in the response body. Array must contain at least 1 object.
* **Rationale:** Asserts that :code:`/continuous/search` returns an array of :code:`Continuous` objects even when specifying additional filters beyond only :code:`format`. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the continuous object listed in the config file.

* **Request:**

.. code-block:: python

   GET /continuous/search?format=loom&version=1.0&tags=cancer
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "tags": [
         "cancer"
       ],
       "URL": "/continuous.loom",
       "id": "fa057c6d18c44960a1b8b49d065b3889",
       "fileType": "loom",
       "version": "1.0",
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR :code:`Array Length < 1`

Continuous Search URL Params Cases
###################################
* **Route:** :code:`/continuous/search`
* **Description:** Sends multiple requests to the endpoint, each time using a different parameter filter in the config file (required :code:`format` parameter is suppled for each request). Expects an array of :code:`Continuous` objects, with length of 1 or greater for each request.
* **Rationale:** Asserts that each filtering parameter, besides :code:`format`, can be used independently of one another, and that each filter yields the expected :code:`Continuous` in the search results.

* **Requests:**

.. code-block:: python

   GET /continuous/search?format=loom&version=1.0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

   GET /continuous/search?format=loom&tags=cancer
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response (for each request):**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "tags": [
         "cancer"
       ],
       "URL": "/continuous.loom",
       "id": "fa057c6d18c44960a1b8b49d065b3889",
       "fileType": "loom",
       "version": "1.0",
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec"
     }
   ]

* **Success Criteria:** For ALL requests: :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND :code:`Array Length >= 1`
* **Failure Criteria:** For ANY request: :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR :code:`Array Length < 1`

Continuous Search Filters Out
###############################
* **Route:** :code:`/continuous/search`
* **Description:** Tests that the continuous search endpoint correctly filters out non-matching :code:`Continuous` based on URL parameters. Makes a request to the :code:`/continuous/search` endpoint with invalid filters (not matching any :code:`Continuous`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Continuous` that differ from filters.

* **Request:**

.. code-block:: python

   GET /continuous/search?format=999999999999&version=999999999999&tags=999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`Status Code != 200` OR response body is not an empty array

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

Continuous Search Formats Match
#################################
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
       "tags": [
         "cancer"
       ],
       "URL": "/continuous.loom",
       "id": "fa057c6d18c44960a1b8b49d065b3889",
       "fileType": "loom",
       "version": "1.0",
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Continuous` json AND ALL :code:`Continuous` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Continuous` json OR ANY :code:`Continuous` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Continuous Search No Format Mismatches
#######################################
* **Route:** :code:`/continuous/search`
* **Description:** Search for all continuous, only specifying the required :code:`format` parameter. However, the value of :code:`format` is different from that supplied in the config file. Checks that all :code:`Continuous` in the response array have a :code:`fileType` that matches the requested :code:`format`.
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
         "loom"
       ],
       "filter": "format",
       "description": "expression file format"
     },
     {
       "fieldType": "string",
       "filter": "version",
       "description": "version to search for"
     },
     {
       "fieldType": "string",
       "filter": "tags",
       "description": "semantic tags associated with data"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Search Filters`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Search Filters`

Continuous Endpoint Not Implemented
####################################
* **Route:** :code:`/continuous/<id>`
* **Description:** If the :code:`Continuous` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/continuous/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /continuous/999999999999999
   Accept: application/vnd.loom, text/tab-separated-values, application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`
