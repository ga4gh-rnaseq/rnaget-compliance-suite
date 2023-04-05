API Specification
============================================================

The RNAget specification describes, at maximum, 18 API routes. These routes
are subdivided into 4 groups according to the data type they serve. These routes,
broken down by data type, are as follows:

1. Projects: Serves project-related information. 3 Routes
    
    * :code:`/projects/:id`
    * :code:`/projects`
    * :code:`/projects/filters`

2. Studies: Serves study-related information. 3 Routes

    * :code:`/studies/:id`
    * :code:`/studies`
    * :code:`/studies/filters`

3. Expressions: Handles requests for querying, slicing, and downloading expression matrix data by gene name/id. 6 Routes

    * :code:`/expressions/formats`
    * :code:`/expressions/filters`
    * :code:`/expressions/:id/ticket`
    * :code:`/expressions/:id/bytes`
    * :code:`/expressions/ticket`
    * :code:`/expressions/bytes`

4. Continuous: Handles requests for querying, slicing, and downloading expression matrix data by genomic coordinate. 6 Routes

    * :code:`/continuous/formats`
    * :code:`/continuous/filters`
    * :code:`/continuous/:id/ticket`
    * :code:`/continuous/:id/bytes`
    * :code:`/continuous/ticket`
    * :code:`/continuous/bytes`

Detailed descriptions of each route are available in the 
`specification document <https://github.com/ga4gh-rnaseq/schema/blob/master/README.md>`_.

Important points:

* A server **MAY** implement all 18 API routes
* A server **MAY** have unimplemented routes from the Expressions and/or Continuous data type groups. If a data type group is unimplemented, then **ALL** of the associated routes **MUST** be unplemented. In other words, a server **MUST NOT** implement only some routes for a data type group.
