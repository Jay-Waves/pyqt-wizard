from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from qfluentwidgets import (PushButton,
                            InfoBar, InfoBarIcon, FluentIcon,  ProgressBar,
                            IndeterminateProgressBar, SpinBox, ProgressRing, 
                            IndeterminateProgressRing, Slider)

class MyProgress(QWidget):
    def __init__(self, value, down, up, parent=None):
        '''
        value: default value
        '''
        super().__init__(parent=parent)
        hLayout = QHBoxLayout(self)

        self.progressBar = ProgressBar(self)
        self.progressBar.setTextVisible(True)
        # self.setFixedSize(80, 80)
        self.spinBox = SpinBox(self)
        self.spinBox.valueChanged.connect(self.range_map)
        self.spinBox.setRange(down, up)
        self.down = down
        self.up = up

        hLayout.addWidget(self.progressBar)
        hLayout.addSpacing(20)
        hLayout.addWidget(self.spinBox)
        hLayout.addSpacing(5)
        hLayout.setContentsMargins(0, 5, 0, 0)

        self.spinBox.setValue(value)
    
    def range_map(self, value):
        mapped_val = int(((value-self.down)/(self.up-self.down))*100)
        self.progressBar.setValue(mapped_val)


class MySlider(QWidget):
    def __init__(self, value, down, up, parent=None):
        '''
        value: default value
        '''
        super().__init__(parent=parent)
        hLayout = QHBoxLayout(self)

        self.slider = Slider(Qt.Orientation.Horizontal)
        self.slider.setRange(down, up)
        self.spinBox = SpinBox(self)
        self.spinBox.setRange(down, up)
        self.spinBox.valueChanged.connect(self.setSlider)
        self.slider.valueChanged.connect(self.setSpinBox)

        hLayout.addWidget(self.slider)
        hLayout.addSpacing(20)
        hLayout.addWidget(self.spinBox)
        hLayout.addSpacing(5)
        hLayout.setContentsMargins(0, 5, 0, 0)

        self.spinBox.setValue(value)
        self.slider.setValue(value)

    def setSlider(self, value):
        self.slider.setValue(value)
    
    def setSpinBox(self, value):
        self.spinBox.setValue(value)
    

class MyRangeWidget(QWidget):
    '''virtually express range of zkrp'''
    def __init__(self, down:int, up:int, unit: str|None=None, use_slider=False, parent=None):
        super().__init__(parent=parent)
        vLayout = QVBoxLayout(self)
        upperBound = 2*up - down
        lowerBound = 2*down-up if 2*down-up > 0 else 0
        if use_slider:
            self.downWidget = MySlider(down, lowerBound, upperBound, self)
            self.upWidget = MySlider(up, lowerBound, upperBound, self)
        else:
            self.downWidget = MyProgress(down, lowerBound, upperBound, self)
            self.upWidget = MyProgress(up, lowerBound, upperBound, self)

        vLayout.addWidget(self.downWidget)
        vLayout.addSpacing(10)
        vLayout.addWidget(self.upWidget)
        vLayout.setContentsMargins(0, 0, 0, 0)
