# -*- coding: utf-8 -*-
"""Module compliance_suite.report_server.py

This module contains methods to spin up a small web server to serve final report
results as HTML.

"""

import time
import http.server
import socketserver
import os
import socket
import webbrowser
import sys
import threading

class ReportServer(object):

    def __init__(self):
        self.port = None
        self.httpd = None
        self.thread = None
        self.web_dir = os.path.join(os.path.dirname(__file__), 'web')
        self.cwd = os.getcwd()

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

    def start_mock_server(self, uptime):
        """run server to serve final test report

        Args:
            port (Port): port on which to run the server
        """

        os.chdir(self.web_dir)
        Handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", self.port), Handler)
        print("serving at http://localhost:" + str(self.port), file=sys.stderr)
        webbrowser.open("http://localhost:" + str(self.port))
        print("server will shut down after " + str(uptime) + " seconds")
        self.httpd.serve_forever()

    def serve_thread(self, uptime=3600):
        self.thread = threading.Thread(target=self.start_mock_server,
                                       args=(uptime,))
        self.thread.start()
        time.sleep(uptime)
        self.httpd.shutdown()
        os.chdir(self.cwd)