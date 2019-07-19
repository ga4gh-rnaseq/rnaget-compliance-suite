# -*- coding: utf-8 -*-
"""Module compliance_suite.user_config_parser.py

This module contains class definition for UserConfigParser, which parses and
validates that the user-specified YAML config file is complete and contains no 
errors. Will raise UserConfigException if an error is detected.
"""

import yaml
from compliance_suite.config.constants import ENDPOINTS
from compliance_suite.exceptions.user_config_exception import \
    UserConfigException

class UserConfigParser(object):
    """Parses user-specified YAML config file

    The UserConfigParser accepts the path to a user-specified YAML config file,
    which will determine what servers, routes, and resources are requested.
    Prior to conducting any tests, this object will validate that the config
    file is constructed correctly.

    Attributes:
        config_file (str): path to YAML config file
        d (dict): dictionary object loaded from the YAML
    """

    def __init__(self, config_file):
        """instantiate a UserConfigParser object

        Args:
            config_file (str): path to YAML config file
        """

        self.config_file = config_file
        self.d = None
    
    def parse_config_file(self):
        """parse YAML config file into dictionary object

        This method attempts to load the YAML config file into a dictionary.
        If any problems occur a FileNotFoundError is raised.

        Raises:
            FileNotFoundError
        """

        try:
            with open(self.config_file, "r") as yaml_file:
                self.d = yaml.load(yaml_file, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            raise FileNotFoundError("user config file: " + self.config_file
                                    + " not found")
    
    def validate_config_file(self):
        """validate YAML-loaded dictionary contains all necessary attributes

        This method validates that the dictionary contains all required
        attributes to conduct a full set of tests. It assesses: whether
        server(s) have been specified, and whether project ids, study ids, and
        expression ids have all been correctly specified as well. Raises a
        UserConfigException if any inconsistencies have been found.

        Raises:
            UserConfigException
        """

        server_req_keys_template = {"server_name", "base_url"} 
            # required attributes for server def,
            # can change if implemented set to false
            # for one or more endpoints
        
        try:
            # validate the root element is "servers" and that there is only
            # one root element
            if len(self.d.keys()) != 1:
                raise UserConfigException('"servers" should be the only root '
                    + 'key')
            
            if list(self.d.keys())[0] != "servers":
                raise UserConfigException('"servers" should be the only root '
                    + 'key')

            server_count = 0
            
            # for each server, validate that there are no missing attributes
            # given the list of required server keys above
            for server in self.d["servers"]:
                server_keys = set(list(server.keys()))

                # for the server, all endpoints are expected to be implemented
                # except if specified in the "implemented" config
                obj_implemented = {e: True for e in ENDPOINTS}
                if "implemented" in server_keys:
                    for impl_key in server["implemented"]:
                        if impl_key not in set(ENDPOINTS):
                            raise UserConfigException(
                                impl_key + ' not a valid endpoint'
                            )

                    for obj_type in ENDPOINTS:
                        if obj_type in server["implemented"].keys():
                            if type(server["implemented"][obj_type]) != bool:
                                raise UserConfigException(
                                    'value of implemented:' + obj_type 
                                    + ' must be a boolean')
                            obj_implemented[obj_type] = \
                                server["implemented"][obj_type]
                
                self.d["servers"][server_count]["implemented"] = obj_implemented
                
                server_req_keys = server_req_keys_template.copy()
                server_keys_diff = server_req_keys.difference(server_keys)
                if len(server_keys_diff) > 0:
                    raise UserConfigException(
                        "missing attribute(s) from server " 
                        + str(server_count + 1) + ": " 
                        + ", ".join(sorted(list(server_keys_diff))))

                server_count += 1
        
        # AttributeError converted to UserConfigException
        except AttributeError as e:
            raise UserConfigException("YAML config file could not be parsed. "
                + "Please refer to the template config file.")
