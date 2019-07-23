from compliance_suite.test_elements.test_element import TestElement
import json

class Component(TestElement):
    
    def as_json(self):
        return {
            "status": self.status,
            "cases": [c.as_json() for c in self.test_cases]
        }