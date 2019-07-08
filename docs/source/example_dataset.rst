Example Dataset
===============

The compliance documentation uses the following example dataset to show success
and error conditions for each API test. When running the compliance test application
against a reference server, it is encouraged to run the tests using the server's
own projects, studies, expressions, and continuous objects (specified via the
yaml config file). However, if this data is not yet available, the example 
dataset below can be uploaded to the reference server to satisfy compliance API
testing.

* Project json

    * :download:`Download <data/project.json>`
    * Format: json
    * MD5: e271c0452c5f46683170f27c6b0d5cc0
    * Used for Routes:

        * :code:`/projects/:id` - response body **MUST** be Project json
        * :code:`/projects/search` - each element in response body array **MUST** be Project json

* Study json

    * :download:`Download <data/study.json>`
    * Format: json
    * MD5: 59d993d20e5809c0caa9cc9f52a373bc
    * Used for Routes:

        * :code:`/studies/:id` - response body **MUST** be Study json
        * :code:`/projects/search` - each element in response body array **MUST** be Study json

* Expression json

    * :download:`Download <data/expression.json>`
    * Format: json
    * MD5: ed1188fe712bfb1bb774432aef627f85
    * Used for Routes:

        * :code:`/expressions/:id` - response **MUST** be Expression json
        * :code:`/expressions/search` - each element in response body array **MUST** be Expression json

* Continuous json

    * :download:`Download <data/continuous.json>`
    * Format: json
    * MD5: eb9aa0c53c5f115cf47590ac5ae707b1
    * Used for Routes:  

        * :code:`/continuous/search` - each element in response body array **MUST** be Continuous json

* Continuous loom

    * :download:`Download <data/continuous.loom>`
    * Format: loom
    * MD5: X
    * Used for Routes:  

        * :code:`/continuous/:id` - each element in response body array **MUST** be Continuous json

* Search Filter

    * :download:`Download <data/search_filter.json>`
    * Format: json
    * MD5: 96c55ff734b8d6af7678de3f3d0f8bea
    * Used for Routes:  

        * :code:`/projects/search/filters` - each element in response body array **MUST** be Search Filter json
        * :code:`/studies/search/filters` - each element in response body array **MUST** be Search Filter json
        * :code:`/expressions/search/filters` - each element in response body array **MUST** be Search Filter json
        * :code:`/continuous/search/filters` - each element in response body array **MUST** be Search Filter json
