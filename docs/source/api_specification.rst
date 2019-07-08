API Specification
============================================================

A reference RNAget server will consist of, at maximum, 14 API routes. These routes
are subdivided into 4 groups according to the data type they serve. These routes,
broken down by data type, are as follows:

1. Projects: Serves project-related information. 3 Routes
    
    * GET Project by ID :code:`/projects/:id`
    * GET List of Projects by search criteria :code:`/projects/search`
    * GET List of valid Project search filters :code:`/projects/search/filters`

2. Studies: Serves study-related information. 3 Routes

    * GET Study by ID :code:`/studies/:id`
    * GET List of Studies by search criteria :code:`/studies/search`
    * GET List of valid Study search filters :code:`/studies/search/filters`

3. Expressions: Handles requests for querying, slicing, and downloading expression matrix data by gene name/id. 4 Routes

    * GET Expression by ID :code:`/expressions/:id`
    * GET supported data formats for Expression matrices :code:`/expressions/formats`
    * GET List of Expressions by search criteria :code:`/expressions/search`
    * GET List of valid Expression search filters :code:`/expressions/search/filters`

4. Continuous: Handles requests for querying, slicing, and downloading expression matrix data by genomic coordinate. 4 Routes

    * GET Continuous by ID :code:`/continuous/:id`
    * GET supported data formats for Continuous matrices :code:`/continuous/formats`
    * GET List of Continuous by search criteria :code:`/continuous/search`
    * GET List of valid Continuous search filters :code:`/continuous/search/filters`

Detailed descriptions of each route are available in the 
`specification document <https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_.

Important points:

* A server **MAY** implement all 14 API routes, and is encouraged to do so
* A server **MAY** have unimplemented routes from the Expressions and/or Continuous data type groups. If a data type group is unimplemented, then **ALL** of the associated routes **MUST** be unplemented. In other words, a server **MUST NOT** implement only some routes for a data type group. 
