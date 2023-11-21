import sys
import os
import subprocess
from PyQt6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
from .signal_bus import signalBus
from .user_manager import User

class Backend(QThread):
    def __init__(self):
        super().__init__()
        # init in this pwd, get the absolute path
        path = os.path.abspath(__file__)
        self.proof_cmd  = os.path.join(os.path.dirname(path), "test_rangeproof_arbitrary")
        self.test_cmd  = os.path.join(os.path.dirname(path), "test_rangeproof_arbitrary")

    def proving(self):
        with subprocess.Popen(self.proof_cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                universal_newlines=True) as p:
            output, _ = p.communicate()
            signalBus.proof.emit(output)
    
    def test(self):
        with subprocess.Popen(self.test_cmd, 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            universal_newlines=True) as p:
            signalBus.test.emit(p.stdout)

    def write_to_log(self, data):
        with open(User.getLogPath(), "a") as log:
            log.write(data)

    def read_from_log(self):
        with open(User.getLogPath(), "r") as f:
            return f.read()

zkrp = Backend()