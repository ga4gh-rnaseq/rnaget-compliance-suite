Test Dataset
===============

This page contains links to test dataset files. The compliance suite expects
the test dataset project, study, expression, and continuous resources to be 
available on the server and accessible by all relevant routes.

* Project json

    * :download:`Download project.json <data/project.json>`
    * id: 9c0eba51095d3939437e220db196e27b
    * Format: json
    * How to Prepare for Compliance Testing
        * upload :code:`project.json` to RNAget server
        * :code:`project.json` **MUST** be accessible by its :code:`id`, ie. :code:`/projects/9c0eba51095d3939437e220db196e27b`
        * :code:`project.json` **MUST** appear in :code:`/projects/search` results array
        * :code:`project.json` **MUST** be filterable by implemented search filters

* Study json

    * :download:`Download <data/study.json>`
    * id: f3ba0b59bed0fa2f1030e7cb508324d1
    * Format: json
    * How to Prepare for Compliance Testing
        * upload :code:`study.json` to RNAget server
        * :code:`study.json` **MUST** be accessible by its :code:`id`, ie. :code:`/studies/f3ba0b59bed0fa2f1030e7cb508324d1`
        * :code:`study.json` **MUST** appear in :code:`/studies/search` results array
        * :code:`study.json` **MUST** be filterable by implemented search filters

* Expression ticket json

    * :download:`Download <data/expression_ticket.json>`
    * id: ac3e9279efd02f1c98de4ed3d335b98e
    * Format: json
    * How to Prepare for Compliance Testing
        * modify :code:`expression_ticket.json` :code:`url` property, so that it points to the test expression matrix file on the server
        * modify :code:`expression_ticket.json` :code:`fileType` property to indicate test expression matrix file format (ie. 'loom' if loom, 'tsv' if tsv)
        * upload modified :code:`expression_ticket.json` to RNAget server
        * :code:`expression_ticket.json` **MUST** be accessible by its :code:`id`, ie. :code:`/expressions/ac3e9279efd02f1c98de4ed3d335b98e/ticket`
        * a valid ticket must be returned for requests for an expression ticket pertaining to the compliance dataset (e.g. :code:`/expressions/ticket?format=loom&studyID=f3ba0b59bed0fa2f1030e7cb508324d1`

* Expression loom

    * :download:`Download <data/expression.loom>`
    * id: ac3e9279efd02f1c98de4ed3d335b98e
    * Format: loom
    * How to Prepare for Compliance Testing
        * upload :code:`expression.loom` **ONLY** if :code:`expression_ticket.json` :code:`fileType` property was set to 'loom'
        * if uploaded, make :code:`expression.loom` accessible by the url in the :code:`url` property of :code:`expression_ticket.json`
        * if uploaded, :code:`expression.loom` must be sliceable by all subsetting parameters (featureIDList, featureNameList, sampleIDList) 

* Expression tsv
    
    * :download:`Download <data/expression.tsv>`
    * id: ac3e9279efd02f1c98de4ed3d335b98e
    * Format: tsv
    * How to Prepare for Compliance Testing
        * upload :code:`expression.tsv` **ONLY** if :code:`expression_ticket.json` :code:`fileType` property was set to 'tsv'
        * if uploaded, make :code:`expression.tsv` accessible by the url in the :code:`url` property of :code:`expression_ticket.json`
        * if uploaded, :code:`expression.tsv` must be sliceable by all subsetting parameters (featureIDList, featureNameList, sampleIDList) 

* Continuous ticket json

    * :download:`Download <data/continuous_ticket.json>`
    * id: 5e22e009f41fc53cbea094a41de8798f
    * Format: json
    * How to Prepare for Compliance Testing
        * modify :code:`continuous_ticket.json` :code:`url` property, so that it points to the test continuous matrix file on the server
        * modify :code:`continuous_ticket.json` :code:`fileType` property to indicate test continuous matrix file format (ie. 'loom' if loom, 'tsv' if tsv)
        * upload modified :code:`continuous_ticket.json` to RNAget server
        * :code:`continuous_ticket.json` **MUST** be accessible by its :code:`id`, ie. :code:`/continuous/5e22e009f41fc53cbea094a41de8798f/ticket`
        * a valid ticket must be returned for requests for a continuous ticket pertaining to the compliance dataset (e.g. :code:`/continuous/ticket?format=loom&studyID=f3ba0b59bed0fa2f1030e7cb508324d1`
        
* Continuous loom

    * :download:`Download <data/continuous.loom>`
    * id: 5e22e009f41fc53cbea094a41de8798f
    * Format: loom
    * How to Prepare for Compliance Testing
        * upload :code:`continuous.loom` **ONLY** if :code:`continuous_ticket.json` :code:`fileType` property was set to 'loom'
        * if uploaded, make :code:`continuous.loom` accessible by the url in the :code:`url` property of :code:`continuous_ticket.json`
        * if uploaded, :code:`continuous.loom` must be sliceable by all subsetting parameters (chr, start, end)

* Continuous tsv

    * :download:`Download <data/continuous.tsv>`
    * id: 5e22e009f41fc53cbea094a41de8798f
    * Format: tsv
    * How to Prepare for Compliance Testing
        * upload :code:`continuous.tsv` **ONLY** if :code:`continuous_ticket.json` :code:`fileType` property was set to 'tsv'
        * if uploaded, make :code:`continuous.tsv` accessible by the url in the :code:`url` property of :code:`continuous_ticket.json`
        * if uploaded, :code:`continuous.tsv` must be sliceable by all subsetting parameters (chr, start, end)

* Filter json

    * :download:`Download <data/filter.json>`
    * Format: json
    * How to Prepare for Compliance Testing
        * :code:`filter.json` is an example, this file does not need to be uploaded, but requests for supported filters must respond with an array of valid :code:`filter` objects

* Error json

    * :download:`Download <data/error.json>`
    * Format: json
    * How to Prepare for Compliance Testing
        * :code:`error.json` is an example, this file does not need to be uploaded, but requests that produce an error must respond with a valid :code:`Error` json object
        * valid :code:`Error` json objects **MUST** at least contain a "message" property
