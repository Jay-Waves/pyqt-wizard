# coding:utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QEvent
from PyQt6.QtGui import QDesktopServices, QPainter, QPen, QColor, QTextCursor
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QListWidget, QStackedWidget, QListWidgetItem

from qfluentwidgets import (ScrollArea, PushButton, FluentIcon,
                            IconWidget, Theme, TitleLabel, 
                            BodyLabel, toggleTheme, TextEdit, EditableComboBox,
                            SwitchButton)
from ..common.config import cfg, FEEDBACK_URL, HELP_URL, EXAMPLE_URL
from ..common.icon import Icon
from ..common.style_sheet import StyleSheet
from ..backend.signal_bus import signalBus
from ..backend.zkrp import zkrp
import random


class ToolBar(QWidget):
    """ Tool bar 
    
    title
    ---
    switch button
    editable combobox
    ---
    parameters select/input
    range input (card: add button, refresh button, test button(verify + proof))
    ---
    update on terminal
    """

    def __init__(self, title, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)

        # test samples input
        self.add_button = PushButton('Add', self, FluentIcon.ADD)
        self.refresh_button = PushButton('Refresh', self, FluentIcon.SYNC)
        self.test_button = PushButton('Begin Test', self, FluentIcon.PLAY_SOLID)
        # a < x < b
        self.a = TextEdit()
        self.b = TextEdit()
        self.x = TextEdit()
        self.lt1 = BodyLabel('<')
        self.lt2 = BodyLabel('<')
        self.range_layout = QHBoxLayout()

        self.vBoxLayout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()

        # params input
        self.range_dim = ParamsCombox('测试范围最大维度数')
        self.base = ParamsCombox('基底')
        self.instance= ParamsCombox('测试实例数')
        self.repeat= ParamsCombox('问询次数')
        self.rs_extra_dimension= ParamsCombox('RS编码裕度')
        self.security_parameter = ParamsCombox('安全参数')
        self.field_size_bits= ParamsCombox('有限域体积')

        # switchs
        self.auto_test = SwitchButton('随机生成测试样例')
        self.auto_test.setOnText('随机生成测试样例')
        self.interactive = SwitchButton('交互式证明')
        self.interactive.setOnText('非交互式证明')
        self.interactive.setChecked(True)
        self.auto_test.checkedChanged.connect(self.onAutoTest)


        self._initWidget()
        self._initSlots()

    def _initWidget(self):
        self.setFixedWidth(300)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addLayout(self.instance)
        self.vBoxLayout.addLayout(self.repeat)
        self.vBoxLayout.addLayout(self.range_dim)
        self.vBoxLayout.addLayout(self.base)
        self.vBoxLayout.addLayout(self.rs_extra_dimension)
        self.vBoxLayout.addLayout(self.security_parameter)
        self.vBoxLayout.addLayout(self.field_size_bits)
        self.vBoxLayout.addSpacing(40)
        self.vBoxLayout.addLayout(self.range_layout)
        self.vBoxLayout.addSpacing(10)
        self.vBoxLayout.addLayout(self.button_layout)
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.auto_test)
        self.vBoxLayout.addWidget(self.interactive)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # set default params
        self.range_dim.combox.addItems(['2^4', '2^8', '2^12', '2^16'])
        self.base.combox.addItems(['2','3', '4', '8', '10', '16'])
        self.instance.combox.addItems(['2^5', '2^7', '2^9', '2^11'])
        self.repeat.combox.addItems(['100', '50', '20', '10', '1'])
        self.security_parameter.combox.addItems(['32', '64', '128', '256', '512'])
        self.rs_extra_dimension.combox.addItems(['3', '5', '7', '11', '17'])
        self.field_size_bits.combox.addItem('63')

        # button layout
        self.button_layout.setSpacing(5)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addWidget(self.test_button)

        # range layout: a < x < b
        self.range_layout.addWidget(self.a)
        self.range_layout.addWidget(self.lt1)
        self.range_layout.addWidget(self.x)
        self.range_layout.addWidget(self.lt2)
        self.range_layout.addWidget(self.b)
        self.range_layout.setContentsMargins(0, 0, 0, 0)
        self.range_layout.setSpacing(5)
        self.a.setPlaceholderText('Lower\nLimits')
        self.b.setPlaceholderText('Upper\nLimits')
        self.x.setPlaceholderText('Variable\nToProve')

    def _initSlots(self):
        self.refresh_button.clicked.connect(self.onRefresh)
        self.test_button.clicked.connect(self.onTest)
        self.add_button.clicked.connect(self.onAdd)

    def onRefresh(self):
        signalBus.test_refresh.emit()
        self.a.clear()
        self.b.clear()
        self.x.clear()

    def onAutoTest(self):
        '''automatically generate random test instances'''
        for _ in range(100):
            txta = random.randint(1, 100)
            txtb = random.randint(101, 500)
            txtx = random.randint(txta, txtb)
            text = f'Add Test Range:  {txta}  <  {txtx}  <  {txtb}'
            signalBus.test.emit(text)

    def onAdd(self):
        '''add new range'''
        txta = self.a.toPlainText()
        if not txta:
            signalBus.test.emit('Warning: Empty Lower Limits!')
            return 
        txtb = self.b.toPlainText()
        if not txtb:
            signalBus.test.emit('Warning: Empty Upper Limits!')
            return
        txtx = self.a.toPlainText()
        if not txta:
            signalBus.test.emit('Warning: Empty Variables To Prove!')
            return
        signalBus.test.emit(f'新测试范围: {txta} < {txtx} < {txtb}')
        self.a.clear()
        self.b.clear()
        self.x.clear()

    def onTest(self):
        zkrp.test()

class ParamsCombox(QHBoxLayout):
    def __init__(self, params_name: str):
        super().__init__()
        self.combox = EditableComboBox()
        self.combox.setFixedWidth(150)
        self.label = BodyLabel(params_name)
        self.addWidget(self.label)
        self.addWidget(self.combox)
        self.setContentsMargins(0, 0, 0, 0)
        self.combox.textChanged.connect(self._onParamsUpdate)

    def _onParamsUpdate(self):
        signalBus.test.emit(f'测试参数变动: [{self.label.text()}]: '+self.combox.currentText())
        

class GalleryInterface(ScrollArea):
    """ Gallery interface 
    ToolBar || Terminal
    """

    def __init__(self, title: str, parent=None):
        """
        Parameters
        ----------
        title: str
            The title of gallery

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar(title, self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.terminal = TextEdit(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.hBoxLayout.addWidget(self.toolBar)
        self.hBoxLayout.addWidget(self.terminal)

        self.view.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

        signalBus.test.connect(self._update_terminal)
        signalBus.test_refresh.connect(self._refresh_termnial)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())

    def _update_terminal(self, line):
        self.terminal.append(line.rstrip())
    
    def _refresh_termnial(self):
        self.terminal.clear()


class TestInterface(GalleryInterface):
    """ Dialog interface """

    def __init__(self, parent=None):
        super().__init__(
            title='后端测试界面',
            parent=parent
        )
        self.setObjectName('testInterface')