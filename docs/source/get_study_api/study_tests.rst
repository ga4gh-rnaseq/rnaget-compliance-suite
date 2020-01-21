Study Tests
===================

This page outlines the success and failure criteria for all tests of Study resources.

Study API Tests
-----------------

Study API tests assert the correct configuration of study-related API 
routes. In order for a test case to succeed, the following conditions must be
met when evaluating the response:
    
    * For all cases, :code:`Content-Type` checking is enforced. The response **MUST** have a :code:`Content-Type` header of :code:`application/vnd.ga4gh.rnaget.v1.0.0+json` OR :code:`application/json`
    * For all cases, :code:`Status Code` checking is enforced. The response **MUST** have the expected status code
    * For all cases, schema checking is enforced. The json object in the response body **MUST** conform to a pre-defined schema of required fields and data types, which is specific to each API route

Study API Test Cases
----------------------

* `Get Test Study`_
* `Study Not Found`_
* `Study Filters`_
* `Search Studies Without Filters`_
* `Search Studies With All Filters`_
* `Search Studies With Single Filter, 1`_
* `Search Studies With Single Filter, 2`_
* `Study Search Filters Non-Matching Resources`_

Get Test Study
#################
* **Route:** :code:`/studies/<id>`
* **Description:** Requests test study by its :code:`id`. Expects the returned study to match the :code:`Study` json schema.
* **Rationale:** Asserts that the :code:`/studies/<id>` endpoint returns **one** valid study object, with id matching the request.

* **Request:**

.. code-block:: python

   GET /studies/f3ba0b59bed0fa2f1030e7cb508324d1
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "id": "f3ba0b59bed0fa2f1030e7cb508324d1",
     "version": "1.0",
     "name": "RNAgetTestStudy0",
     "description": "Test study object used by RNAget compliance testing suite.",
     "parentProjectID": "9c0eba51095d3939437e220db196e27b"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is valid :code:`Study` json
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT valid :code:`Study` json

Study Not Found
######################
* **Route:** :code:`/studies/<id>`
* **Description:** Requests a study with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Study` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/studies/<id>` endpoint does not return arbitrary :code:`Study` objects, and only returns a :code:`Study` when the :code:`id` matches.

* **Request:**

.. code-block:: python

   GET /studies/nonexistentid9999999999999999999
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

Study Filters
#######################
* **Route:** :code:`/studies/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Studies`
* **Rationale:** Asserts that the endpoint returns an array of :code:`filter` objects

* **Request:**

.. code-block:: python

   GET /studies/filters
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
       "values": [
         "PCAWG",
         "RNAGetTestStudy0"
       ],
       "filter": "name",
       "description": "name of study"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`filters`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`filters`

Search Studies Without Filters
################################
* **Route:** :code:`/studies`
* **Description:** Searches for all studies, without specifying any filtering parameters. Expects an array of :code:`Studies` in the response body.
* **Rationale:** Asserts that the :code:`/studies` returns an array, and that each element in the array is a :code:`Study`.

* **Request:**

.. code-block:: python

   GET /studies
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "6cccbbd76b9c4837bd7342dd616d0fec",
       "parentProjectID": "43378a5d48364f9d8cf3c3d5104df560",
       "name": "PCAWG",
       "description": "PCAWG study",
       "version": "1.0"
     },
     {
       "id": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "parentProjectID": "9c0eba51095d3939437e220db196e27b",
       "name": "RNAgetTestStudy0",
       "description": "Test study object used by RNAget compliance testing suite.",
       "version": "1.0"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Study` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Study` json OR :code:`Array Length < 1`

Search Studies With All Filters
#################################
* **Route:** :code:`/studies`
* **Description:** Searches studies, using all filtering parameters associated with test study. Expects an array of :code:`Studies` to be returned in the response body. Array must contain at least 1 object.
* **Rationale:** Asserts that :code:`/studies` returns an array of :code:`Studies` even when specifying filters. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the test study.

* **Request:**

.. code-block:: python

   GET /studies?version=1.0&name=RNAgetTestStudy0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "parentProjectID": "9c0eba51095d3939437e220db196e27b",
       "name": "RNAgetTestStudy0",
       "description": "Test study object used by RNAget compliance testing suite.",
       "version": "1.0"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Study` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Study` json OR :code:`Array Length < 1`

Search Studies With Single Filter, 1
######################################
* **Route:** :code:`/studies`
* **Description:** Searches studies using only 1 filtering parameter associated with test study. Expects an array of :code:`Studies`, with length of 1 or greater.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields the test :code:`Study` in the search results.

* **Requests:**

.. code-block:: python

   GET /studies?version=1.0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "parentProjectID": "9c0eba51095d3939437e220db196e27b",
       "name": "RNAgetTestStudy0",
       "description": "Test study object used by RNAget compliance testing suite.",
       "version": "1.0"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Study` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Study` json OR :code:`Array Length < 1`

Search Studies With Single Filter, 2
######################################
* **Route:** :code:`/studies`
* **Description:** Searches studies using only 1 filtering parameter (a different filter than above) associated with test study. Expects an array of :code:`Studies`, with length of 1 or greater.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields the test :code:`Study` in the search results.

* **Requests:**

.. code-block:: python

   GET /studies?name=RNAgetTestStudy0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "f3ba0b59bed0fa2f1030e7cb508324d1",
       "parentProjectID": "9c0eba51095d3939437e220db196e27b",
       "name": "RNAgetTestStudy0",
       "description": "Test study object used by RNAget compliance testing suite.",
       "version": "1.0"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Study` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Study` json OR :code:`Array Length < 1`

Study Search Filters Non-Matching Resources
##############################################
* **Route:** :code:`/studies`
* **Description:** Tests that the study search endpoint correctly filters out non-matching :code:`Studies` based on url parameters. Makes a request to the :code:`/studies` endpoint with invalid filters (not matching any :code:`Study`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Studies` that differ from filters.

* **Request:**

.. code-block:: python

   GET /studies?version=nonexistentid9999999999999999999&name=nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT an empty array

Study API Non-Implemented Test Cases
---------------------------------------

* `Study Get Not Implemented`_
* `Study Search Not Implemented`_
* `Study Search Filters Not Implemented`_

Study Get Not Implemented
############################
* **Route:** :code:`/studies/<id>`
* **Description:** If the :code:`Studies` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/studies/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Study` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /studies/nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Study Search Not Implemented
###############################
* **Route:** :code:`/studies`
* **Description:** If the :code:`Studies` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/studies` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Study` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /studies
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Study Search Filters Not Implemented
#######################################
* **Route:** :code:`/studies/filters`
* **Description:** If the :code:`Studies` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/studies/filters` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Study` related endpoints are correctly non-implemented according to the spec

* **Request:**

.. code-block:: python

   GET /studies/filters
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`
