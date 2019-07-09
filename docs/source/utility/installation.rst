Installation
============

This section provides instructions on how to install the RNAget compliance
suite application.

As a prerequisite, python 3 and pip must be installed on your system. The 
application can be installed by running the following from the command line. 

1. Clone the latest build from https://github.com/ga4gh-rnaseq/rnaget-compliance-suite

.. code-block:: bash

    git clone https://github.com/ga4gh-rnaseq/rnaget-compliance-suite

2. Enter rnaget-compliance-suite directory and install

.. code-block:: bash

    cd rnaget-compliance-suite
    python setup.py install

3. Confirm installation by executing the rnaget-compliance command

.. code-block:: bash

    rnaget-compliance report

The `next article <usage.html>`_ explains how to run the compliance application.
