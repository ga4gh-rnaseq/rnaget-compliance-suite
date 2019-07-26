# -*- coding: utf-8 -*-
"""Module compliance_suite.report_server.py

This module contains class definition of small web server utility. Serves final
report results as HTML.
"""

import datetime
import time
import http.server
import socketserver
import os
import logging
import inspect
import socket
import webbrowser
import sys
import threading
import json
import jinja2 as j2
from compliance_suite.config.constants import ENDPOINTS

def capitalize(text):
    """capitalizes a word, for use in rendering template

    Args:
        text (str): word to capitalize
    
    Returns:
        capitalized (str): capitalized word
    """

    return text[0].upper() + text[1:]

def get_route_status(route_obj):

    count_d = {"pass": 0, "fail": 0, "skip": 0, "unknown": 0}
    symbol_d = {"1": "pass", "-1": "fail", "0": "skip", "2": "unknown"}
    ret = {"btn": "btn-success", "text": "Pass"}

    for obj_key in route_obj.keys():
        for test in route_obj[obj_key]:
            count_d[symbol_d[str(test["result"])]] += 1

    if count_d["fail"] > 0 or count_d["skip"] > 0:
        ret = {
            "btn": "btn-danger",
            "text": "%s Failed / %s Skipped" % (str(count_d["fail"]),
                                                str(count_d["skip"]))
        }
    
    return ret


class ReportServer(object):
    """Creates web server, serves test report as HTML

    The ReportServer spins up a small, local web server to host test result
    reports once the final JSON object has been generated. The server can be
    shut down with CTRL+C.

    Attributes:
        port (Port): object representing free port to serve content
        httpd (TCPServer): handle for web server
        thread (Thread): thread serves content indefinitely, can be killed
            safely from the outside via CTRL+C
        web_dir (str): directory which host web files (CSS and generated HTML)
        cwd (str): working directory to change back to after creating server
        render_helper (dict): contains data structures and functions to be
            passed to rendering engine to aid in rendering HTML
    """

    def __init__(self, web_dir):
        """instantiates a ReportServer object"""

        self.port = None
        self.httpd = None
        self.thread = None
        self.web_dir = web_dir
        self.cwd = os.getcwd()
        self.render_helper = {
            "s": { # s: structures
                "endpoints": ENDPOINTS,
                "singles": {
                    "projects": "project",
                    "studies": "study",
                    "expressions": "expression",
                    "continuous": "continuous"
                },
                "status": {
                    0: {
                        "status": "SKIPPED",
                        "css_class": "text-info",
                        "fa_class": "fa-ban"
                    },
                    1: {
                        "status": "PASSED",
                        "css_class": "text-success",
                        "fa_class": "fa-check-circle"
                    },
                    -1: {
                        "status": "FAILED",
                        "css_class": "text-danger",
                        "fa_class": "fa-times-circle"
                    },
                    2: {
                        "status": "UNKNOWN ERROR",
                        "css_class": "text-danger",
                        "fa_class": "fa-times-circle"
                    }
                }
            },
            "f": { # f: functions
                "capitalize": capitalize,
                "format_test_name": lambda text: " ".join(
                    [capitalize(t) for t in text.split("_")]
                ),
                "server_name_url": lambda name: \
                    name.lower().replace(" ", "") + ".html",
                "rm_space": lambda text: text.replace(" ", "_")\
                                             .replace(",", ""),
                "timestamp": lambda: \
                    datetime.datetime.now(datetime.timezone.utc)\
                                     .strftime("%B %d, %Y at %l:%M %p (%Z)"),
                "route_status": get_route_status
            }
        }

    def set_free_port(self):
        """get free port on local machine on which to run the report server

        This function is used in conftest and the return of this is a free port 
        available in the system on which the mock server will be run. This port
        will be passed to start_mock_server as a required parameter from 
        conftest.py

        Returns:
            (Port): free port on which to run server
        """

        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        self.port = port

    def render_html(self):
        data = None
        with open(self.web_dir + "/results.json", "r") as f:
            data = json.load(f)

        # set up jinja2 rendering engine
        view_loader = j2.FileSystemLoader(searchpath=self.web_dir)
        view_env = j2.Environment(loader=view_loader)

        # render the index/homepage
        home_template = view_env.get_template("views/home.html")
        home_rendered = home_template.render(data=data, h=self.render_helper)
        home_path = self.web_dir + "/index.html"
        open(home_path, "w").write(home_rendered)

        for server in data:
            report_template = view_env.get_template("views/report.html")
            report_rendered = report_template.render(server=server,
                                                     h=self.render_helper)
            report_path = self.web_dir + "/" + \
                self.render_helper["f"]["server_name_url"](server["server_name"])
            open(report_path, "w").write(report_rendered)
        
    def start_mock_server(self, uptime):
        """run server to serve final test report

        Args:
            port (Port): port on which to run the server
        """

        os.chdir(self.web_dir)
        Handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", self.port), Handler)
        logging.info("serving at http://localhost:" + str(self.port))
        webbrowser.open("http://localhost:" + str(self.port))
        logging.info("server will shut down after " + str(uptime) + " seconds, "
                     + "press CTRL+C to shut down manually")
        self.httpd.serve_forever()

    def serve_thread(self, uptime=3600):
        """serves server as separate thread so it can be stopped from outside
        
        Args:
            uptime (int): server will remain up for this time in seconds unless
                shutdown by user
        """

        try:
            self.thread = threading.Thread(target=self.start_mock_server,
                                        args=(uptime,))
            self.thread.start()
            time.sleep(uptime)
        except KeyboardInterrupt as e:
            print("stopping server")
        finally:
            self.httpd.shutdown()
            os.chdir(self.cwd)