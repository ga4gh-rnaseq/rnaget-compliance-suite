# -*- coding: utf-8 -*-
"""Module compliance_suite.exceptions.test_status_exception.py

This module contains class definitions for test status exceptions.
"""

class TestStatusException(Exception):
    """Exception for test status exceptions

    A TestStatusException is potentially raised during the set_test_status
    method in the SingleTestExecutor class. If the test fails one of the
    following checks: content type validation, status code validation,
    response body schema validation; then a TestStatusException is raised.
    """
    
    pass

class MediaTypeException(TestStatusException):
    """Raised when response content type does not match accepted media types"""

    pass

class StatusCodeException(TestStatusException):
    """Raised when response status code does not match expected status code"""

    pass

class JsonParseException(TestStatusException):
    """Raised when a JSON object could not be parsed from response body"""

    pass

class SchemaValidationException(TestStatusException):
    """Raised when response body does not match expected object schema"""

    pass

class ContentTestException(TestStatusException):
    """Raised when a content testing function failed"""

    pass