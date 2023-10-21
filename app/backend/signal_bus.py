# coding: utf-8
from PyQt6.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ pyqtSignal bus """

    switchToSampleCard = pyqtSignal(str, int)
    micaEnableChanged = pyqtSignal(bool)
    supportSignal = pyqtSignal()
    newRangeInterface = pyqtSignal(str)
    newProofInterface = pyqtSignal(str) # user name

    proof = pyqtSignal(str) # user name, terminal line
    proof_end = pyqtSignal()
    verify = pyqtSignal(str) # user name, terminal line

signalBus = SignalBus()