import os
import time
import signal
from multiprocessing import Process
from compliance_suite.report_server import ReportServer

def spawn_report_server():
    rs = ReportServer()
    rs.set_free_port()
    rs.serve_thread()

def test_keyboard_interrupt():
    p = Process(target=spawn_report_server)
    p.start()
    time.sleep(2)
    os.kill(p.pid, signal.SIGINT)
    time.sleep(2)
    assert p.is_alive() == False
    assert p.exitcode == 0
