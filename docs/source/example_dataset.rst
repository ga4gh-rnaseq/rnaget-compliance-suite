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
    * MD5: 6fcb61aa19d2d925e17c1ac078449a62
    * Used for Routes:

        * :code:`/expressions/:id` - response **MUST** be Expression json
        * :code:`/expressions/search` - each element in response body array **MUST** be Expression json

* Expression loom

    * :download:`Download <data/expression.loom>`
    * Format: loom
    * MD5: 7c6b3eecd28cf19c8724f36208fa33c1
    * Used for Routes:  

        * :code:`/expressions/:id` - response **MUST** contain a URL to download an expression matrix file as an attachment. File **MAY** be in one of several formats (in this case, loom).

* Continuous json

    * :download:`Download <data/continuous.json>`
    * Format: json
    * MD5: e82610293e3184da7f15b38a258cabdd
    * Used for Routes:  

        * :code:`/continuous/search` - each element in response body array **MUST** be Continuous json

* Continuous loom

    * :download:`Download <data/continuous.loom>`
    * Format: loom
    * MD5: caaedb61eb0d8bdb7e28c5acc3d699d1
    * Used for Routes:  

        * :code:`/continuous/:id` - response **MUST** provide a Continuous signal intensity file as an attachment. File **MAY** be in one of several formats (in this case, loom).

* Search Filter json

    * :download:`Download <data/search_filter.json>`
    * Format: json
    * MD5: 96c55ff734b8d6af7678de3f3d0f8bea
    * Used for Routes:  

        * :code:`/projects/search/filters` - each element in response body array **MUST** be Search Filter json
        * :code:`/studies/search/filters` - each element in response body array **MUST** be Search Filter json
        * :code:`/expressions/search/filters` - each element in response body array **MUST** be Search Filter json
        * :code:`/continuous/search/filters` - each element in response body array **MUST** be Search Filter json

* Error json

    * :download:`Download <data/error.json>`
    * Format: json
    * MD5: 4d353dcbe39e41fee522485e3f965a16
    * Used for Routes:  

        * :code:`/projects/:id` - if a project could not be found, the response body **MUST** be Error json, which specifies an error message
        * :code:`/studies/:id` - if a study could not be found, the response body **MUST** be Error json, which specifies an error message
        * :code:`/expressions/:id` - if an expression could not be found, the response body **MUST** be Error json, which specifies an error message
        * :code:`/continuous/:id` - if a continuous object could not be found, the response body **MUST** be Error json, which specifies an error message
