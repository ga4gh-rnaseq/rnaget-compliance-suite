.. rnaget compliance suite documentation master file, created by
   sphinx-quickstart on Wed Jul  3 13:38:49 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Preamble
============================================================

Welcome to the RNAget Server Compliance documentation.

This documentation (and associated `compliance testing application <https://github.com/ga4gh-rnaseq/rnaget-compliance-suite>`_) determines a
server's compliance with the 
`RNAget API specification <https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_
for serving RNAseq datasets. The specification,
developed by the `Global Alliance for Genomics and Health <https://www.ga4gh.org/>`_, serves to provide a
standardized API framework and data structure to allow for interoperability of datasets
hosted at different institutions.

RNAget Servers
--------------

RNAget Servers enable access to RNAseq datasets and their metadata using unique 
identifiers for each object in a hierarchical data model. Servers can be queried
for expression matrices, as well as project and study information associated 
with the raw RNAseq data. Servers support the slicing of expression matrices by
gene, sample, and/or genomic coordinate, so that only subsets of a large matrix 
need to be transferred.

Compliance Document
-------------------

This documentation is for implementers of RNAget servers. Implementers **MUST**
adhere to this documentation during development of RNAget-compliant servers, as 
the compliance tests outlined herein conform with the 
`RNAget specification <https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_. 
The testing suite performs API testing on all routes discussed in the specification. 
Reference server responses **MUST** comply with the correct responses in this document
for requests made to each route/endpoint.

RNAget maintains an up-to-date report of the compliance status of its reference
implementers. `Click here to view the latest report. <https://ga4gh-rnaseq.github.io/rnaget-compliance-suite/report/>`_

Click `here <api_specification.html>`_ to learn more about the `API Specification <api_specification.html>`_

Table of Contents
------------------

.. toctree::
   :maxdepth: 2
   
   api_specification
   example_dataset

.. toctree::
    :maxdepth: 2
    :caption: GET Project API

    get_project_api/project_tests

.. toctree::
    :maxdepth: 2
    :caption: GET Study API
    
    get_study_api/study_tests

.. toctree::
    :maxdepth: 2
    :caption: GET Expression API
    
    get_expression_api/expression_tests

.. toctree::
    :maxdepth: 2
    :caption: GET Continuous API
    
    get_continuous_api/continuous_tests

.. toctree::
   :maxdepth: 2
   :caption: Compliance Utility

   utility/getting_started
   utility/installation
   utility/usage
   utility/report
