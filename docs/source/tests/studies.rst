Studies
========

`back to tests overview <overview.html>`_

Study-related tests
---------------------

* `Study Get`_
* `Study Get Not Found`_
* `Study Search`_
* `Study Search URL Params All`_
* `Study Search URL Params Cases`_
* `Study Search Filters Out`_
* `Study Search Filters`_
* `Study Endpoint Not Implemented`_

Study Get
-----------
* **Route:** :code:`/studies/<id>`
* **Description:** Requests a study with the :code:`id` from the yaml config. Expects the specified study to be returned in json format, and matching the :code:`Study` schema.
* **Rationale:** Asserts that the :code:`/studies/<id>` endpoint returns **one** valid study object, with id matching the request.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Study`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Study`

Study Get Not Found
---------------------
* **Route:** :code:`/studies/<id>`
* **Description:** Requests a study with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Study` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/studies/<id>` endpoint does not return arbitrary :code:`Study` objects, and only returns a :code:`Study` when the :code:`id` matches.
* **Success Criteria:** :code:`status_code == 404` AND reponse body is valid json of type :code:`Error`
* **Failure Criteria:** :code:`status_code != 404` OR reponse body is NOT valid json of type :code:`Error`

Study Search
--------------
* **Route:** :code:`/studies/search`
* **Description:** Searches for all studies, without specifying any filtering parameters. Expects a :code:`Study Array` to be returned in the response body.
* **Rationale:** Asserts that the :code:`/studies/search` returns an array, and that each element in the array is of type :code:`Study`.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Study Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Study Array` OR :code:`Array Length < 1`

Study Search URL Params All
-----------------------------
* **Route:** :code:`/studies/search`
* **Description:** Searches studies, using all filtering parameters specified in the config file. Expects a :code:`Study Array` to be returned in the response body, and for the array to contain at least 1 object.
* **Rationale:** Asserts that the :code:`/studies/search` returns an array of :code:`Study` objects even when specifying filters. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the study listed in the config file.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Study Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Study Array` OR :code:`Array Length < 1`

Study Search URL Params Cases
-------------------------------
* **Route:** :code:`/studies/search`
* **Description:** Sends multiple requests to the endpoint, each time using a different parameter filter in the config file. Expects a :code:`Study Array` of at least 1 :code:`Study` for each request.
* **Rationale:** Asserts that each filtering parameter can be used independently of one another, and that each filter yields the expected :code:`Study` in the search results.
* **Success Criteria:** For ALL requests: :code:`status_code == 200` AND response body is valid json of type :code:`Study Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** For ANY request: :code:`status_code != 200` OR response body is NOT valid json of type :code:`Study Array` OR :code:`Array Length < 1`

Study Search Filters Out
--------------------------
* **Route:** :code:`/studies/search`
* **Description:** Tests that the study search endpoint correctly filters out non-matching :code:`Studies` based on URL parameters. Makes a request to the :code:`/studies/search` endpoint with invalid filters (not matching any :code:`Study`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Studies` that differ from filters.
* **Success Criteria:** :code:`status_code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`status_code != 200` OR response body is not an empty array

Study Search Filters
----------------------
* **Route:** :code:`/studies/search/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Studies`
* **Rationale:** Asserts that the endpoint returns an array of :code:`Search Filter` objects
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Search Filter Array`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Search Filter Array`

Study Endpoint Not Implemented
--------------------------------
* **Route:** :code:`/studies/<id>`
* **Description:** If the :code:`Studies` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/studies/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Study` related endpoints are correctly non-implemented according to the spec 
* **Success Criteria:** :code:`status_code == 501`
* **Failure Criteria:** :code:`status_code != 501`