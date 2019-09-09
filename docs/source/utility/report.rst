Report
==================

Once the compliance report has been generated, the HTML report can be accessed by
first starting a web server at the output directory, then navigating to the page
via web browser.

Viewing the Report
------------------

Report: Index
##############

The report index page displays a tabular overview of test successes/failures by
tested servers and API routes. An example report index is displayed below:

.. image:: ../_images/rnaget-compliance-report-index-1.jpg
    :align: left
    :alt: alternate text

Clicking on any of the *Pass*/*Fail* buttons will take you to an in-depth report
of the status of all tests for that server.

Report: Test Status
#######################

This page shows a more detailed report of all tests run on a particular server,
organized by API route and test case. For any given test, clicking the *Info*
button will display information for that test, including the request url, 
parameters, and the response body. The *Info* window is also helpful in 
diagnosing failed compliance tests, as it reports the type of error 
encountered and related debug messages.

Below is an example of *Projects* test results for one server in the test
status page:

.. image:: ../_images/rnaget-compliance-report-test-1.jpg
    :align: left
    :alt: alternate text

Clicking the *Info* button shows test information, displayed below:

.. image:: ../_images/rnaget-compliance-report-test-2.jpg
    :align: left
    :alt: alternate text

Test results can also be viewed as a matrix:

.. image:: ../_images/rnaget-compliance-report-test-matrix.jpg
    :align: left
    :alt: alternate text
