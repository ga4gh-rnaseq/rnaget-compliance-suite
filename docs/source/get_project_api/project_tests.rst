Project Tests
===================

This page outlines the success and error conditions for all tests of Project API routes.

Important Points

* In order for a test to succeed, the following conditions must be met when evaluating the response
    
    * For all tests, :code:`Content-Type` checking is enforced. The response **MUST** have a :code:`Content-Type` header of :code:`application/vnd.ga4gh.rnaget.v1.0.0+json` OR :code:`application/json`
    * For all tests, :code:`Status Code` checking is enforced. The response **MUST** have the expected status code
    * For all tests, schema checking is enforced. The json object in the response body **MUST** conform to a pre-defined schema of required fields and data types, which is specific to each API route

Project test cases are discussed below

Project Test Cases
######################

* `Project Get`_
* `Project Get Not Found`_
* `Project Search`_
* `Project Search URL Params All`_
* `Project Search URL Params Cases`_
* `Project Search Filters Out`_
* `Project Search Filters`_
* `Project Endpoint Not Implemented`_

Project Get
#################
* **Route:** :code:`/projects/<id>`
* **Description:** Requests a project by its :code:`id`. Expects the returned project to match the :code:`Project` json schema.
* **Rationale:** Asserts that the :code:`/projects/<id>` endpoint returns **one** valid project object, with id matching the request.

* **Request:**

.. code-block:: python

   GET /projects/43378a5d48364f9d8cf3c3d5104df560
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

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

* **Success Criteria:** :code:`Status Code == 200` AND response body is valid :code:`Project json`
* **Error Criteria:** :code:`Status Code != 200` OR response body is NOT valid :code:`Project json`

Project Get Not Found
######################
* **Route:** :code:`/projects/<id>`
* **Description:** Requests a project with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Project` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/projects/<id>` endpoint does not return arbitrary :code:`Project` objects, and only returns a :code:`Project` when the :code:`id` matches.

* **Request:**

.. code-block:: python

   GET /projects/999999999999999
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 404 Not Found
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   {
     "message": "Entry not found in database."
   }

* **Success Criteria:** :code:`status_code == 404` AND reponse body is valid :code:`Error` json
* **Failure Criteria:** :code:`status_code != 404` OR reponse body is NOT valid :code:`Error` json

Project Search
#################
* **Route:** :code:`/projects/search`
* **Description:** Searches for all projects, without specifying any filtering parameters. Expects an array of :code:`Projects` in the response body.
* **Rationale:** Asserts that the :code:`/projects/search` returns an array, and that each element in the array is a :code:`Project`.

* **Request:**

.. code-block:: python

   GET /projects/search
   Accept: application/vnd.ga4gh.rnaget.v1.0.0+json, application/json

* **Successful Response:**

.. code-block:: python

   HTTP/1.1 200 OK
   Content-Type: application/vnd.ga4gh.rnaget.v1.0.0+json

   [
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

* **Success Criteria:** :code:`status_code == 200` AND response body is array of :code:`Project` json AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT array of :code:`Project` json OR :code:`Array Length < 1`

Project Search URL Params All
##############################
* **Route:** :code:`/projects/search`
* **Description:** Searches projects, using all filtering parameters specified in the config file. Expects a :code:`Project Array` to be returned in the response body, and for the array to contain at least 1 object.
* **Rationale:** Asserts that the :code:`/projects/search` returns an array of :code:`Project` objects even when specifying filters. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the project listed in the config file.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Project Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Project Array` OR :code:`Array Length < 1`

Project Search URL Params Cases
##################################
* **Route:** :code:`/projects/search`
* **Description:** Sends multiple requests to the endpoint, each time using a different parameter filter in the config file. Expects a :code:`Project Array` of at least 1 :code:`Project` for each request.
* **Rationale:** Asserts that each filtering parameter can be used independently of one another, and that each filter yields the expected :code:`Project` in the search results.
* **Success Criteria:** For ALL requests: :code:`status_code == 200` AND response body is valid json of type :code:`Project Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** For ANY request: :code:`status_code != 200` OR response body is NOT valid json of type :code:`Project Array` OR :code:`Array Length < 1`

Project Search Filters Out
##################################
* **Route:** :code:`/projects/search`
* **Description:** Tests that the project search endpoint correctly filters out non-matching :code:`Projects` based on URL parameters. Makes a request to the :code:`/projects/search` endpoint with invalid filters (not matching any :code:`Project`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Projects` that differ from filters.
* **Success Criteria:** :code:`status_code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`status_code != 200` OR response body is not an empty array

Project Search Filters
#######################
* **Route:** :code:`/projects/search/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Projects`
* **Rationale:** Asserts that the endpoint returns an array of :code:`Search Filter` objects
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Search Filter Array`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Search Filter Array`

Project Endpoint Not Implemented
##################################
* **Route:** :code:`/projects/<id>`
* **Description:** If the :code:`Projects` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/projects/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Project` related endpoints are correctly non-implemented according to the spec 
* **Success Criteria:** :code:`status_code == 501`
* **Failure Criteria:** :code:`status_code != 501`