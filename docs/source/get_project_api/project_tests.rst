Project Tests
===================

This page outlines the success and failure criteria for all tests of Project resources.

Project API Tests
-----------------

Project API tests assert the correct configuration of project-related API 
routes. In order for a test case to succeed, the following conditions must be
met when evaluating the response:
    
    * For all cases, :code:`Content-Type` checking is enforced. The response **MUST** have a :code:`Content-Type` header of :code:`application/vnd.ga4gh.rnaget.v1.0.0+json` OR :code:`application/json`
    * For all cases, :code:`Status Code` checking is enforced. The response **MUST** have the expected status code
    * For all cases, schema checking is enforced. The json object in the response body **MUST** conform to a pre-defined schema of required fields and data types, which is specific to each API route

Project API Test Cases
----------------------

* `Get Test Project`_
* `Project Not Found`_
* `Project Filters`_
* `Search Projects Without Filters`_
* `Search Projects With All Filters`_
* `Search Projects With Single Filter, 1`_
* `Search Projects With Single Filter, 2`_
* `Project Search Filters Non-Matching Resources`_

Get Test Project
#################
* **Route:** :code:`/projects/<id>`
* **Description:** Requests test project by its :code:`id`. Expects the returned project to match the :code:`Project` json schema.
* **Rationale:** Asserts that the :code:`/projects/<id>` endpoint returns **one** valid project object, with id matching the request.

* **Request:**

.. code-block:: python

   GET /projects/9c0eba51095d3939437e220db196e27b
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
      "id": "9c0eba51095d3939437e220db196e27b",
      "version": "1.0",
      "name": "RNAgetTestProject0",
      "description": "Test project object used by RNAget compliance testing suite.",
      "tags": [
         "RNAgetCompliance"
      ]
   }

* **Success Criteria:** :code:`Status Code == 200` AND response body is valid :code:`Project` json
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT valid :code:`Project` json

Project Not Found
######################
* **Route:** :code:`/projects/<id>`
* **Description:** Requests a project with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Project` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/projects/<id>` endpoint does not return arbitrary :code:`Project` objects, and only returns a :code:`Project` when the :code:`id` matches.

* **Request:**

.. code-block:: python

   GET /projects/nonexistentid9999999999999999999
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

Project Filters
#######################
* **Route:** :code:`/projects/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Projects`
* **Rationale:** Asserts that the endpoint returns an array of :code:`Filter` objects

* **Request:**

.. code-block:: python

   GET /projects/filters
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
         "RNAgetTestProject0"
       ],
       "filter": "name",
       "description": "name of project"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Filters`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Filters`

Search Projects Without Filters
################################
* **Route:** :code:`/projects`
* **Description:** Searches for all projects, without specifying any filtering parameters. Expects an array of :code:`Projects` in the response body.
* **Rationale:** Asserts that :code:`/projects` returns an array, and that each element in the array is a :code:`Project`.

* **Request:**

.. code-block:: python

   GET /projects
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "9c0eba51095d3939437e220db196e27b",
       "version": "1.0",
       "name": "RNAgetTestProject0",
       "description": "Test project object used by RNAget compliance testing suite.",
       "tags": [
         "RNAgetCompliance"
       ]
     },
     {
       "tags": [
         "PCAWG",
         "cancer"
       ],
       "description": "Pan Cancer Analysis of Whole Genomes test data from Expression Atlas E-MTAB-5423",
       "id": "43378a5d48364f9d8cf3c3d5104df560",
       "name": "PCAWG",
       "version": "1.0"
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Project` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Project` json OR :code:`Array Length < 1`

Search Projects With All Filters
#################################
* **Route:** :code:`/projects`
* **Description:** Searches projects, using all filtering parameters associated with test project. Expects an array of :code:`Projects` to be returned in the response body. Array must contain at least 1 object.
* **Rationale:** Asserts that :code:`/projects` returns an array of :code:`Projects` even when specifying filters. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the test project.

* **Request:**

.. code-block:: python

   GET /projects?version=1.0&name=RNAgetTestProject0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "9c0eba51095d3939437e220db196e27b",
       "version": "1.0",
       "name": "RNAgetTestProject0",
       "description": "Test project object used by RNAget compliance testing suite.",
       "tags": [
         "RNAgetCompliance"
       ]
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Project` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Project` json OR :code:`Array Length < 1`

Search Projects With Single Filter, 1
######################################
* **Route:** :code:`/projects`
* **Description:** Searches projects using only 1 filtering parameter associated with test project. Expects an array of :code:`Projects`, with length of 1 or greater.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields the test :code:`Project` in the search results.

* **Requests:**

.. code-block:: python

   GET /projects?version=1.0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "9c0eba51095d3939437e220db196e27b",
       "version": "1.0",
       "name": "RNAgetTestProject0",
       "description": "Test project object used by RNAget compliance testing suite.",
       "tags": [
         "RNAgetCompliance"
       ]
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Project` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Project` json OR :code:`Array Length < 1`

Search Projects With Single Filter, 2
######################################
* **Route:** :code:`/projects`
* **Description:** Searches projects using only 1 filtering parameter (a different filter than above) associated with test project. Expects an array of :code:`Projects`, with length of 1 or greater.
* **Rationale:** Asserts filtering parameters can be used independently of one another, and that each filter yields the test :code:`Project` in the search results.

* **Requests:**

.. code-block:: python

   GET /projects?name=RNAgetTestProject0
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
     {
       "id": "9c0eba51095d3939437e220db196e27b",
       "version": "1.0",
       "name": "RNAgetTestProject0",
       "description": "Test project object used by RNAget compliance testing suite.",
       "tags": [
         "RNAgetCompliance"
       ]
     }
   ]

* **Success Criteria:** :code:`Status Code == 200` AND response body is array of :code:`Project` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT array of :code:`Project` json OR :code:`Array Length < 1`

Project Search Filters Non-Matching Resources
##############################################
* **Route:** :code:`/projects`
* **Description:** Tests that the project search endpoint correctly filters out non-matching :code:`Projects` based on url parameters. Makes a request to the :code:`/projects` endpoint with invalid filters (not matching any :code:`Project`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Projects` that differ from filters.

* **Request:**

.. code-block:: python

   GET /projects?version=nonexistentid9999999999999999999&name=nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   []

* **Success Criteria:** :code:`Status Code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`Status Code != 200` OR response body is NOT an empty array

Project API Non-Implemented Test Cases
---------------------------------------

* `Project Get Not Implemented`_
* `Project Search Not Implemented`_
* `Project Filters Not Implemented`_

Project Get Not Implemented
############################
* **Route:** :code:`/projects/<id>`
* **Description:** If the :code:`Projects` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/projects/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Project` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /projects/nonexistentid9999999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Project Search Not Implemented
###############################
* **Route:** :code:`/projects`
* **Description:** If the :code:`Projects` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/projects` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Project` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /projects
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`

Project Filters Not Implemented
#######################################
* **Route:** :code:`/projects/filters`
* **Description:** If the :code:`Projects` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/projects/filters` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Project` related endpoints are correctly non-implemented according to the spec 

* **Request:**

.. code-block:: python

   GET /projects/filters
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 501 Not Implemented
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

* **Success Criteria:** :code:`Status Code == 501`
* **Failure Criteria:** :code:`Status Code != 501`
