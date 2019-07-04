Projects
========

`back to tests overview <overview.html>`_

Project-related tests
---------------------

* `Project Get`_
* `Project Get Not Found`_
* `Project Search`_
* `Project Search URL Params All`_
* `Project Search URL Params Cases`_
* `Project Search Filters Out`_
* `Project Search Filters`_

Project Get
-----------
* Route: :code:`/projects/<id>`
* Parameters: None
* Description: Requests a project with the :code:`id` from the yaml config. Expects the specified project to be returned in JSON format, and matching the :code:`Project` schema.
* Rationale: Asserts that the :code:`/projects/<id>` endpoint returns **one** valid project object, with id matching the request.
* Success Criteria: :code:`status_code == 200` AND response body is valid JSON of type :code:`Project`
* Failure Criteria: :code:`status_code != 200` OR response body is NOT valid JSON of type :code:`Project`

Project Get Not Found
---------------------

Project Search
--------------

Project Search URL Params All
-----------------------------

Project Search URL Params Cases
-------------------------------

Project Search Filters Out
--------------------------

Project Search Filters
----------------------