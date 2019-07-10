Usage
==========================

The application can be run from the command line with the following command:

.. code-block:: bash

    rnaget-compliance report

Command line parameters are as follows:

.. csv-table:: rnaget-compliance report command line parameters
   :header: "Parameter", "Short Name", "Required?", "Description"
   :widths: 10 2 2 20

   "--user-config", "-c", "Yes", "Path to yaml file, indicating which server(s), project(s), expression(s), etc. to query"
   "--output_dir", "-o", "No", "Output directory to write report results and web files. Directory must not already exist. Defaults to ./rnaget-compliance-results if not specified"
   "--serve", "N/A", "No", "Flag. If set, the program will spin up a local server serving the HTML report after all compliance tests are completed."
   "--uptime", "-u", "No", "Integer. The local report server will shut down automatically after this time in seconds."
   "--no-tar", "N/A", "No", "Flag. If set, the program will not write a .tar.gz archive of report results"

User Config YAML File
---------------------

The compliance application requires configurations to be written to a YAML file,
which is specified on the command line. The following is a template of the config
file, which can be modified to query different servers, projects, studies, etc.

.. code-block:: bash

    servers:
      - server_name: Caltech
        base_url: https://felcat.caltech.edu/rnaget/
        implemented:
          projects: true
          studies: true
          expressions: true
          continuous: true

        projects:
          - id: 43378a5d48364f9d8cf3c3d5104df560
            filters:
              version: 1.0

        studies:
          - id: 6cccbbd76b9c4837bd7342dd616d0fec
            filters:
              version: 1.0

        expressions:
          - id: 2a7ab5533ef941eaa59edbfe887b58c4
            filters:
              studyID: 6cccbbd76b9c4837bd7342dd616d0fec
              format: loom

        continuous:
          - id: fa057c6d18c44960a1b8b49d065b3889
            filters:
              version: 1.0
              format: loom

The .yml config file contains the following important features, which must be
taken into consideration when modifying it for a different server:

1. *servers* must be the root property. The value of *servers* is a list of server definitions (ie the application can query multiple servers in a single run).
2. Each server definition requires the following parameters:
    
    * server_name: a string uniquely identifying the server 
    * base_url: the base URL at which the RNAGet API can be reached

3. If a server requires client authentication, then a server definition can include the OAuth 2.0 bearer access token under the "token" property:

.. code-block:: bash

   servers:
      - server_name: Caltech
        base_url: https://felcat.caltech.edu/rnaget/
        token: abcdefghijklmnop
        implemented:
          projects: true
          studies: true
          expressions: true
          continuous: true

The token will be used for all API tests executed by the compliance suite.

4. A server's *implemented* property indicates which routes (projects, studies, expressions, continuous) have been implemented. This property can be removed if all routes are implemented, as routes are expected to be implemented by default. Use :code:`${ROUTENAME}: false` to indicate non-implemented routes.
5. All implemented routes must have their own property (ie servers implementing *projects* must contain an object with the :code:`projects` property). Each property contains a list of object definitions.

.. code-block:: bash

    projects:
      - id: 43378a5d48364f9d8cf3c3d5104df560
        filters:
          version: 1.0

The above definition specifies a list of one project object that is expected to
be available on the target server. Each object definition must specify the 
:code:`id` at which it can be reached (via the :code:`/${OBJECT}/<id>` route), 
as well as a key:value map of filter names and values under the :code:`filters`
property. Filters will be applied to test the :code:`/${OBJECT}/search` route with
query/search parameters.

6. If :code:`expressions` or :code:`continuous` endpoints are implemented, each 
expression and continuous object must contain the :code:`format` property as 
one of their :code:`filters`. The specification requires that :code:`format` be
specified for search requests to the :code:`/expressions/search` and 
:code:`/continuous/search` endpoints.

Basic Usage
-----------

The program requires, at minimum, a YAML config file to be specified in order 
to execute:

.. code-block:: bash

    rnaget-compliance report -c user_config_template.yaml

The user can also specify the location at which to create the output report
directory. The program will only run if the output directory does not already
exist (will not overwrite existing files):

.. code-block:: bash

    rnaget-compliance report -c user_config_template.yaml -o ./results/output

The program creates a series of web files at the output directory, which can be
used to view the compliance results as an HTML report. A web server can be 
started manually at the output directory to serve the report. By specifying the
:code:`--serve` option, the report server will be started automatically upon
completion of the compliance tests:

.. code-block:: bash

    rnaget-compliance report -c user_config_template.yaml -o ./results/output --serve

The `next article <report.html>`_ explains how to view the compliance report, 
including how to diagnose errors (compliance failures)
