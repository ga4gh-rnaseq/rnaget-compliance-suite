.. rnaget compliance suite documentation master file, created by
   sphinx-quickstart on Wed Jul  3 13:38:49 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation for the rnaget compliance suite
============================================================

The rnaget-compliance-suite application determines a server's compliance with
the `RNAget API specification <https://github.com/ga4gh-rnaseq/schema/blob/master/rnaget.md>`_ for serving RNAseq datasets. The specification,
developed by the `Global Alliance for Genomics and Health <https://www.ga4gh.org/>`_, serves to provide a
standardized API framework and data structure to allow for interoperability of datasets
hosted at different institutions. The compliance application can test new 
services for compliance to the specification, and can diagnose where a 
non-compliant service falls short of the specficiation.

If you have an RNAseq dataset that you would like to serve in an 
RNAGet-compliant manner, click `here to get started <usage/preparation.html>`_.


.. toctree::
   :maxdepth: 2
   :caption: Usage

   usage/preparation
   usage/installation
   usage/usage
   usage/report

.. toctree::
   :maxdepth: 2
   :caption: Tests by API Route

   tests/overview
   tests/projects
   tests/studies
   tests/expressions
   tests/continuous
