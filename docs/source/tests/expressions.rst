Expressions
===========

`back to tests overview <overview.html>`_

Expressions-related tests
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
---------------
* **Route:** :code:`/expressions/<id>`
* **Description:** Requests an expression with the :code:`id` from the yaml config. Expects the specified expression to be returned in json format, and matching the :code:`Expression` schema.
* **Rationale:** Asserts that the :code:`/expression/<id>` endpoint returns **one** valid expression object, with id matching the request.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Expression`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Expression`

Expression Get Not Found
-------------------------
* **Route:** :code:`/expressions/<id>`
* **Description:** Requests an expression with an invalid :code:`id`, that is, an :code:`id` that does not correspond to any :code:`Expression` on the server. Expects a :code:`404 Not Found` status code in the response, and a response body with a message explaining that the specified resource could not be found.
* **Rationale:** Asserts that the :code:`/expressions/<id>` endpoint does not return arbitrary :code:`Expression` objects, and only returns an :code:`Expression` when the :code:`id` matches.
* **Success Criteria:** :code:`status_code == 404` AND reponse body is valid json of type :code:`Error`
* **Failure Criteria:** :code:`status_code != 404` OR reponse body is NOT valid json of type :code:`Error`

Expression Formats
-------------------
* **Route:** :code:`/expressions/formats`
* **Description:** Requests the available expression data file formats on the server. Expects a :code:`String Array` of formats to be returned in the response body.
* **Rationale:** Asserts that :code:`/expressions/formats` returns a :code:`String Array` of expression file formats the server supports
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`String Array`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`String Array`

Expression Search
------------------
* **Route:** :code:`/expressions/search`
* **Description:** Searches for all expressions, only specifying the required :code:`format` parameter. Expects an :code:`Expression Array` to be returned in the response body.
* **Rationale:** Asserts that the :code:`/expressions/search` returns an array, and that each element in the array is of type :code:`Expression`.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Expression Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Expression Array` OR :code:`Array Length < 1`

Expression Search URL Params All
--------------------------------
* **Route:** :code:`/expressions/search`
* **Description:** Searches expressions, using all filtering parameters specified in the config file. Expects an :code:`Expression Array` to be returned in the response body, and for the array to contain at least 1 object.
* **Rationale:** Asserts that :code:`/expressions/search` returns an array of :code:`Expression` objects even when specifying additional filters beyond only :code:`format`. The returned array MUST have at least 1 object, as the parameter filters must match the attributes of the expression listed in the config file.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Expression Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Expression Array` OR :code:`Array Length < 1`

Expression Search URL Params Cases
-----------------------------------
* **Route:** :code:`/expressions/search`
* **Description:** Sends multiple requests to the endpoint, each time using a different parameter filter in the config file (required :code:`format` parameter is suppled for each request). Expects a :code:`Expression Array` of at least 1 :code:`Expression` for each request.
* **Rationale:** Asserts that each filtering parameter, besides :code:`format`, can be used independently of one another, and that each filter yields the expected :code:`Expression` in the search results.
* **Success Criteria:** For ALL requests: :code:`status_code == 200` AND response body is valid json of type :code:`Expression Array` AND :code:`Array Length >= 1`
* **Failure Criteria:** For ANY request: :code:`status_code != 200` OR response body is NOT valid json of type :code:`Expression Array` OR :code:`Array Length < 1`

Expression Search Filters Out
-----------------------------
* **Route:** :code:`/expressions/search`
* **Description:** Tests that the expression search endpoint correctly filters out non-matching :code:`Expressions` based on URL parameters. Makes a request to the :code:`/expressions/search` endpoint with invalid filters (not matching any :code:`Expression`), and expects an empty array as a response.
* **Rationale:** Asserts that the endpoint correctly filters out non-matching entities, that the endpoint does not return an arbitrary list of :code:`Expressions` that differ from filters.
* **Success Criteria:** :code:`status_code == 200` AND response body is an empty array
* **Failure Criteria:** :code:`status_code != 200` OR response body is not an empty array

Expression Search Format Not Specified
--------------------------------------
* **Route:** :code:`/expressions/search`
* **Description:** Searches for all expressions WITHOUT specifying the required :code:`format` parameter. Expects a :code:`4xx` error response, with an error message indicating that the request was invalid.
* **Rationale:** As the :code:`format` parameter is required to specify file format for the :code:`/expressions/search` endpoint, this test asserts malformed requests raise an error.
* **Success Criteria:** :code:`status_code == 4xx` AND reponse body is valid json of type :code:`Error`
* **Failure Criteria:** :code:`status_code != 4xx` AND reponse body is NOT valid json of type :code:`Error`

Expression Search Filetypes Match
--------------------------------------
* **Route:** :code:`/expressions/search`
* **Description:** Search for all expressions, only specifying the required :code:`format` parameter. Checks that all :code:`Expressions` in the response array have a :code:`fileType` that matches the requested :code:`format`.
* **Rationale:** Asserts that the :code:`/expressions/<id>` endpoint does not return arbitrary :code:`Expressions`, only :code:`Expressions` with a :code:`fileType` matching the requested :code:`format`.
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Expression Array` AND ALL :code:`Expressions` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Expression Array` OR ANY :code:`Expression` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Expression Search No Filetype Mismatches
-----------------------------------------
* **Route:** :code:`/expressions/search`
* **Description:** Search for all expressions, only specifying the required :code:`format` parameter. However, the value of :code:`format` is different from that supplied in the config file. Checks that all :code:`Expressions` in the response array have a :code:`fileType` that matches the requested :code:`format`.
* **Rationale:** This test is used in conjunction with the above to ensure that only :code:`Expressions` of the correct :code:`fileType` are returned. Asserts that all :code:`Expressions` returned from the above test case are excluded from the response of this test case
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Expression Array` AND ALL :code:`Expressions` have a :code:`fileType` matching the requested :code:`format`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Expression Array` OR ANY :code:`Expression` DOES NOT have a :code:`fileType` matching the requested :code:`format`

Expression Search Filters
--------------------------
* **Route:** :code:`/expressions/search/filters`
* **Description:** Requests the filters that can be used to narrow search results for a list of :code:`Expressions`
* **Rationale:** Asserts that the endpoint returns an array of :code:`Search Filter` objects
* **Success Criteria:** :code:`status_code == 200` AND response body is valid json of type :code:`Search Filter Array`
* **Failure Criteria:** :code:`status_code != 200` OR response body is NOT valid json of type :code:`Search Filter Array`

Expression Endpoint Not Implemented
-----------------------------------
* **Route:** :code:`/expressions/<id>`
* **Description:** If the :code:`Expressions` endpoint is specified as :code:`Not Implemented` in the config file, then this test will be run. Requests the :code:`/expressions/<id>` endpoint, expecting a :code:`501 Not Implemented` status code response
* **Rationale:** Asserts that :code:`Expression` related endpoints are correctly non-implemented according to the spec 
* **Success Criteria:** :code:`status_code == 501`
* **Failure Criteria:** :code:`status_code != 501`