Expression Tests
===================

This page outlines the success and failure criteria for all tests of Expression API routes.

Important Points

* In order for a test to succeed, the following conditions must be met when evaluating the response
    
    * For all tests, :code:`Content-Type` checking is enforced. The response **MUST** have a :code:`Content-Type` header of :code:`application/vnd.ga4gh.rnaget.v1.0.0+json` OR :code:`application/json`
    * For all tests, :code:`Status Code` checking is enforced. The response **MUST** have the expected status code
    * For all tests, schema checking is enforced. The json object in the response body **MUST** conform to a pre-defined schema of required fields and data types, which is specific to each API route

Expression test cases are discussed below

Expression Test Cases
--------------------------

* `Expression Get`_
* `Expression Get Not Found`_
* `Expression Formats`_
* `Expression Search`_
* `Expression Search URL Params All`_
* `Expression Search URL Params Cases`_
* `Expression Search Filters Out`_
* `Expression Search Format Not Specified`_
* `Expression Search Filetypes Match`_
* `Expression Search No Filetype Mismatches`_
* `Expression Search Filters`_
* `Expression Endpoint Not Implemented`_

Expression Get
###############
* **Route:** :code:`/expressions/<id>`
* **Description:** Requests an expression by its :code:`id`. Expects the returned expression to match the :code:`Expression` json schema.
* **Rationale:** Asserts that the :code:`/expression/<id>` endpoint returns **one** valid expression object, with id matching the request.

* **Request:**

.. code-block:: python

   GET /expressions/2a7ab5533ef941eaa59edbfe887b58c4
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
     "URL": "/expression.loom",
     "id": "2a7ab5533ef941eaa59edbfe887b58c4",
     "units": "TPM",
     "fileType": "loom"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is valid :code:`Expression` json
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT valid :code:`Expression` json

Expression Get Not Found
#########################
* **Route:** :code:`/expressions/<id>`
* **Description:** Requests an expression with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Expression` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/expressions/<id>` endpoint does not return arbitrary :code:`Expression` objects, and only returns an :code:`Expression` when the :code:`id` matches.

* **Request:**

.. code-block:: python

   GET /expressions/999999999999999
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

Expression Formats
###################
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
     "loom"
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is an array of strings in json format
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT an array of strings in json format

Expression Search
##################
* **Route:** :code:`/expressions/search`
* **Description:** Searches for all expressions, only specifying the required :code:`format` parameter. Expects an array of :code:`Expressions` in the response body.
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
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "URL": "/expression.loom",
       "id": "2a7ab5533ef941eaa59edbfe887b58c4",
       "units": "TPM",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR :code:`Array Length < 1`

Expression Search URL Params All
#################################
* **Route:** :code:`/expressions/search`
* **Description:** Searches expressions, using all filtering parameters specified in the config file. Expects an array of :code:`Expressions` to be returned in the response body. Array must contain at least 1 object.
* **Rationale:** Asserts that :code:`/expressions/search` returns an array of :code:`Expressions` even when specifying additional filters beyond only :code:`format`. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the expression listed in the config file.

* **Request:**

.. code-block:: python

   GET /expressions/search?format=loom&studyID=6cccbbd76b9c4837bd7342dd616d0fec&units=TPM
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "URL": "/expression.loom",
       "id": "2a7ab5533ef941eaa59edbfe887b58c4",
       "units": "TPM",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR :code:`Array Length < 1`

Expression Search URL Params Cases
###################################
* **Route:** :code:`/expressions/search`
* **Description:** Sends multiple requests to the endpoint, each time using a different parameter filter in the config file (required :code:`format` parameter is suppled for each request). Expects an array of :code:`Expressions`, with length of 1 or greater for each request.
* **Rationale:** Asserts that each filtering parameter, besides :code:`format`, can be used independently of one another, and that each filter yields the expected :code:`Expression` in the search results.

* **Requests:**

.. code-block:: python

   GET /expressions/search?format=loom&studyID=6cccbbd76b9c4837bd7342dd616d0fec
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

   GET /expressions/search?format=loom&units=TPM
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response (for each request):**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "URL": "/expression.loom",
       "id": "2a7ab5533ef941eaa59edbfe887b58c4",
       "units": "TPM",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** For ALL requests: :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND :code:`Array Length >= 1`
* **Failure Criteria:** For ANY request: :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR :code:`Array Length < 1`

Expression Search Filters Out
##############################
* **Route:** :code:`/expressions/search`
* **Description:** Tests that the expression search endpoint correctly filters out non-matching :code:`Expressions` based on URL parameters. Makes a request to the :code:`/expressions/search` endpoint with invalid filters (not matching any :code:`Expression`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Expressions` that differ from filters.

* **Request:**

.. code-block:: python

   GET /expressions/search?format=999999999999&studyID=999999999999&name=999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`Status Code != 200` OR response body is not an empty array

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
       "studyID": "6cccbbd76b9c4837bd7342dd616d0fec",
       "URL": "/expression.loom",
       "id": "2a7ab5533ef941eaa59edbfe887b58c4",
       "units": "TPM",
       "fileType": "loom"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Expression` json AND ALL :code:`Expressions` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Expression` json OR ANY :code:`Expression` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Expression Search No Filetype Mismatches
#########################################
* **Route:** :code:`/expressions/search`
* **Description:** Search for all expressions, only specifying the required :code:`format` parameter. However, the value of :code:`format` is different from that supplied in the config file. Checks that all :code:`Expressions` in the response array have a :code:`fileType` that matches the requested :code:`format`.
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
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT valid json of type :code:`Expression Array` OR ANY :code:`Expression` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Expression Search Filters
##########################
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
         "loom"
       ],
       "filter": "format",
       "description": "expression file format"
     },
     {
       "fieldType": "string",
       "filter": "studyID",
       "description": "study associated with the expression"
     },
     {
       "fieldType": "string",
       "values": [
         "TPM"
       ],
       "filter": "units",
       "description": "units for expression values in matrix file"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Search Filters`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Search Filters`

Expression Endpoint Not Implemented
#####################################
* **Route:** :code:`/expressions/<id>`
* **Description:** If the :code:`Expressions` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/expressions/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /expressions/999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`