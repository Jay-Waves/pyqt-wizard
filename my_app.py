# coding:utf-8
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from app.common.config import cfg
from app.view.main_window import MainWindow

# enable dpi scale
if cfg.get(cfg.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

# create main window
w = MainWindow()
w.show()

app.exec()
