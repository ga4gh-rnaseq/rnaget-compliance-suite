# Development

## New endpoint

Add configuration data for the new endpoint:

- edit config package files
  - add API endpoint to `constants.py`
  - add tests to `tests.py`
  - add child/parent relationships to `graph.py`
- create schema file in `schemas` and add it to `constants.py`

Modify test execution logic to include the new endpoint

- add endpoint key in `tests.py` to:
  - `obj_type_placeholders`
  - `test_obj_dict` 
  - `initiate_tests` for loops
- add endpoint key in `test_runner.py` to:
  - `self.results`