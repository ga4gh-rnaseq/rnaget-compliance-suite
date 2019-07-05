Continuous
===========

`back to tests overview <overview.html>`_

Continuous-related tests
--------------------------

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
---------------
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests continuous data with the :code:`id` from the yaml config. Expects signal intensity to be returned as a file attachment.
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint returns a signal intensity file as an attachment.
* **Success Criteria:** :code:`status_code == 200` AND :code:`Content-Type` corresponds to the file :code:`format` (loom, tsv, etc.)
* **Failure Criteria:** :code:`status_code != 200` OR :code:`Content-Type` DOES NOT correspond to the file :code:`format` (loom, tsv, etc.)

Continuous Get Not Found
-------------------------
* **Route:** :code:`/continuous/<id>`
* **Description:** Requests a continuous with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Continuous` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint does not return arbitrary :code:`Continuous` data, and only returns :code:`Continuous` data when the :code:`id` matches.
* **Success Criteria:** :code:`status_code == 404` AND reponse body is valid json of type :code:`Error`
* **Failure Criteria:** :code:`status_code != 404` OR reponse body is NOT valid json of type :code:`Error`

Continuous Formats
-------------------
* **Route:** :code:`/continuous/formats`
* **Description:** Requests the available continuous data file formats on the server. Expects a :code:`String Array` of formats to be returned in the response body.
* **Rationale:** Asserts that :code:`/continuous/formats` returns a :code:`String Array` of continuous file formats the server supports
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`String Array`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`String Array`

Continuous Search
------------------
* **Route:** :code:`/continuous/search`
* **Description:** Searches for all continuous objects, only specifying the required :code:`format` parameter. Expects a :code:`Continuous Array` to be returned in the response body.
* **Rationale:** Asserts that the :code:`/continuous/search` returns an array, and that each element in the array is of type :code:`Continuous`.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Continuous Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Continuous Array` OR :code:`Array Length < 1`

Continuous Search URL Params All
--------------------------------
* **Route:** :code:`/continuous/search`
* **Description:** Searches continuous objects, using all filtering parameters specified in the config file. Expects a :code:`Continuous Array` to be returned in the response body, and for the array to contain at least 1 object.
* **Rationale:** Asserts that :code:`/continuous/search` returns an array of :code:`Continuous` objects even when specifying additional filters beyond only :code:`format`. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the continuous object listed in the config file.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Continuous Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Continuous Array` OR :code:`Array Length < 1`

Continuous Search URL Params Cases
-----------------------------------
* **Route:** :code:`/continuous/search`
* **Description:** Sends multiple requests to the endpoint, each time using a different parameter filter in the config file (required :code:`format` parameter is suppled for each request). Expects a :code:`Continuous Array` of at least 1 :code:`Continuous` for each request.
* **Rationale:** Asserts that each filtering parameter, besides :code:`format`, can be used independently of one another, and that each filter yields the expected :code:`Continuous` in the search results.
* **Success Criteria:** For ALL requests: :code:`status_code == 200` AND response body is valid json of type :code:`Continuous Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** For ANY request: :code:`status_code != 200` OR response body is NOT valid json of type :code:`Continuous Array` OR :code:`Array Length < 1`

Continuous Search Filters Out
-----------------------------
* **Route:** :code:`/continuous/search`
* **Description:** Tests that the continuous search endpoint correctly filters out non-matching :code:`Continuous` based on URL parameters. Makes a request to the :code:`/continuous/search` endpoint with invalid filters (not matching any :code:`Continuous`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Continuous` that differ from filters.
* **Success Criteria:** :code:`status_code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`status_code != 200` OR response body is not an empty array

Continuous Search Format Not Specified
--------------------------------------
* **Route:** :code:`/continuous/search`
* **Description:** Searches for all continuous WITHOUT specifying the required :code:`format` parameter. Expects a :code:`4xx` error response, with an error message indicating that the request was invalid.
* **Rationale:** As the :code:`format` parameter is required to specify file format for the :code:`/continuous/search` endpoint, this test asserts malformed requests raise an error.
* **Success Criteria:** :code:`status_code == 4xx` AND reponse body is valid json of type :code:`Error`
* **Failure Criteria:** :code:`status_code != 4xx` AND reponse body is NOT valid json of type :code:`Error`

Continuous Search Formats Match
--------------------------------------
* **Route:** :code:`/continuous/search`
* **Description:** Search for all continuous, only specifying the required :code:`format` parameter. Checks that all :code:`Continuous` in the response array have a :code:`fileType` that matches the requested :code:`format`.
* **Rationale:** Asserts that the :code:`/continuous/<id>` endpoint does not return arbitrary :code:`Continuous`, only :code:`Continuous` with a :code:`fileType` matching the requested :code:`format`.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Continuous Array` AND ALL :code:`Continuous` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Continuous Array` OR ANY :code:`Continuous` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Continuous Search No Format Mismatches
-----------------------------------------
* **Route:** :code:`/continuous/search`
* **Description:** Search for all continuous, only specifying the required :code:`format` parameter. However, the value of :code:`format` is different from that supplied in the config file. Checks that all :code:`Continuous` in the response array have a :code:`fileType` that matches the requested :code:`format`.
* **Rationale:** This test is used in conjunction with the above to ensure that only :code:`Continuous` of the correct :code:`fileType` are returned. Asserts that all :code:`Continuous` returned from the above test case are excluded from the response of this test case
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Continuous Array` AND ALL :code:`Continuous` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Continuous Array` OR ANY :code:`Continuous` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Continuous Search Filters
--------------------------
* **Route:** :code:`/continuous/search/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Continuous`
* **Rationale:** Asserts that the endpoint returns an array of :code:`Search Filter` objects
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Search Filter Array`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Search Filter Array`

Continuous Endpoint Not Implemented
-----------------------------------
* **Route:** :code:`/continuous/<id>`
* **Description:** If the :code:`Continuous` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/continuous/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Continuous` related endpoints are correctly non-implemented according to the spec 
* **Success Criteria:** :code:`status_code == 501`
* **Failure Criteria:** :code:`status_code != 501`
