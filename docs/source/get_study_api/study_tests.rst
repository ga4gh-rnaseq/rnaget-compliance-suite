Study Tests
===================

This page outlines the success and failure criteria for all tests of Study API routes.

Important Points

* In order for a test to succeed, the following conditions must be met when evaluating the response
    
    * For all tests, :code:`Content-Type` checking is enforced. The response **MUST** have a :code:`Content-Type` header of :code:`application/vnd.ga4gh.rnaget.v1.0.0+json` OR :code:`application/json`
    * For all tests, :code:`Status Code` checking is enforced. The response **MUST** have the expected status code
    * For all tests, schema checking is enforced. The json object in the response body **MUST** conform to a pre-defined schema of required fields and data types, which is specific to each API route

Study test cases are discussed below

Study Test Cases
-----------------

* `Study Get`_
* `Study Get Not Found`_
* `Study Search`_
* `Study Search URL Params All`_
* `Study Search URL Params Cases`_
* `Study Search Filters Out`_
* `Study Search Filters`_
* `Study Endpoint Not Implemented`_

Study Get
###########
* **Route:** :code:`/studies/<id>`
* **Description:** Requests a study by its :code:`id`. Expects the returned study to match the :code:`Study` json schema.
* **Rationale:** Asserts that the :code:`/studies/<id>` endpoint returns **one** valid study object, with id matching the request.

* **Request:**

.. code-block:: python

   GET /studies/6cccbbd76b9c4837bd7342dd616d0fec
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "version": "1.0",
     "id": "6cccbbd76b9c4837bd7342dd616d0fec",
     "name": "PCAWG",
     "description": "PCAWG study",
     "tags": [
       "PCAWG",
       "cancer"
     ],
     "parentProjectID": "43378a5d48364f9d8cf3c3d5104df560"
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is valid :code:`Study` json
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT valid :code:`Study` json

Study Get Not Found
####################
* **Route:** :code:`/studies/<id>`
* **Description:** Requests a study with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Study` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/studies/<id>` endpoint does not return arbitrary :code:`Study` objects, and only returns a :code:`Study` when the :code:`id` matches.

* **Request:**

.. code-block:: python

   GET /studies/999999999999999
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

Study Search
##############
* **Route:** :code:`/studies/search`
* **Description:** Searches for all studies, without specifying any filtering parameters. Expects an array of :code:`Studies` to be returned in the response body.
* **Rationale:** Asserts that the :code:`/studies/search` returns an array, and that each element in the array is a :code:`Study`.

* **Request:**

.. code-block:: python

   GET /studies/search
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "version": "1.0",
       "id": "6cccbbd76b9c4837bd7342dd616d0fec",
       "name": "PCAWG",
       "description": "PCAWG study",
       "tags": [
         "PCAWG",
         "cancer"
       ],
       "parentProjectID": "43378a5d48364f9d8cf3c3d5104df560"
     } 
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Study` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Study` json OR :code:`Array Length < 1`

Study Search URL Params All
############################
* **Route:** :code:`/studies/search`
* **Description:** Searches studies, using all filtering parameters specified in the config file. Expects an array of :code:`Studies` to be returned in the response body. Array must contain at least 1 object.
* **Rationale:** Asserts that :code:`/studies/search` returns an array of :code:`Studies` even when specifying filters. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the study listed in the config file.

* **Request:**

.. code-block:: python

   GET /studies/search?version=1.0&name=PCAWG
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "version": "1.0",
       "id": "6cccbbd76b9c4837bd7342dd616d0fec",
       "name": "PCAWG",
       "description": "PCAWG study",
       "tags": [
         "PCAWG",
         "cancer"
       ],
       "parentProjectID": "43378a5d48364f9d8cf3c3d5104df560"
     } 
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Study` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Study` json OR :code:`Array Length < 1`

Study Search URL Params Cases
##############################
* **Route:** :code:`/studies/search`
* **Description:** Sends multiple requests to the endpoint, each time using a different parameter filter in the config file. Expects an array of :code:`Studies`, with length of 1 or greater for each request.
* **Rationale:** Asserts that each filtering parameter can be used independently of one another, and that each filter yields the expected :code:`Study` in the search results.

* **Requests:**

.. code-block:: python

   GET /studies/search?version=1.0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

   GET /studies/search?name=PCAWG
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response (for each request):**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "version": "1.0",
       "id": "6cccbbd76b9c4837bd7342dd616d0fec",
       "name": "PCAWG",
       "description": "PCAWG study",
       "tags": [
         "PCAWG",
         "cancer"
       ],
       "parentProjectID": "43378a5d48364f9d8cf3c3d5104df560"
     } 
   ]

* **Success Criteria:** For ALL requests: :code:`Status Code == 200` AND response body is array of :code:`Study` json AND :code:`Array Length >= 1`
* **Failure Criteria:** For ANY request: :code:`Status Code != 200` OR response body is NOT array of :code:`Study` json OR :code:`Array Length < 1`

Study Search Filters Out
#########################
* **Route:** :code:`/studies/search`
* **Description:** Tests that the study search endpoint correctly filters out non-matching :code:`Studies` based on URL parameters. Makes a request to the :code:`/studies/search` endpoint with invalid filters (not matching any :code:`Study`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Studies` that differ from filters.

* **Request:**

.. code-block:: python

   GET /studies/search?version=999999999999&name=999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`Status Code != 200` OR response body is not an empty array

Study Search Filters
#####################
* **Route:** :code:`/studies/search/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Studies`
* **Rationale:** Asserts that the endpoint returns an array of :code:`Search Filter` objects

* **Request:**

.. code-block:: python

   GET /studies/search/filters
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
         "PCAWG"
       ],
       "filter": "name",
       "description": "name of associated project"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Search Filters`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Search Filters`

Study Endpoint Not Implemented
###############################
* **Route:** :code:`/studies/<id>`
* **Description:** If the :code:`Studies` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/studies/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Study` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /studies/999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`