# coding: utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl, QSize
from PyQt6.QtGui import QIcon, QDesktopServices, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget, QLineEdit

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen, setTheme, Theme, MessageBoxBase, SubtitleLabel, LineEdit)
from qfluentwidgets import FluentIcon as FIF

from .home_interface import HomeInterface
from .proof_interface import ProofInterface
from .log_interface import LogInterface
# from .layout_interface import LayoutInterface
from .request_interface import RequestInterface
from .test_interface import TestInterface
from .range_interface import RangeInterface
from .setting_interface import SettingInterface
from ..common.config import SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common import resource
from ..backend.signal_bus import signalBus
from ..backend.user_manager import User 


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        self.loginWindow = LoginMessageBox(self.window()) 
        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.requestInterface = RequestInterface('DefineRangePage', self)
        self.logInterface = LogInterface(self)
        self.settingInterface = SettingInterface(self)
        self.proofInterface = ProofInterface(self)
        self.testInterface = TestInterface(self)
        self.rangePages = []

        self.connectSignalToSlot()
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        # signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.showMsgBox)
        signalBus.newRangeInterface.connect(self._addRangeInterface)
        User.userLogin.connect(self._login)
        User.userExit.connect(self._exit)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, '首页')
        self.addSubInterface(self.requestInterface, FIF.PENCIL_INK, '制定放贷标准')
        self.addSubInterface(self.logInterface, FIF.COMMAND_PROMPT, '日志信息')
        self.addSubInterface(self.testInterface, FIF.PALETTE, '后端测试')
        self.navigationInterface.addSeparator()

        scroll_pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.proofInterface, FIF.FINGERPRINT, '收到的征信证明', position=scroll_pos)
        self.navigationInterface.addItem('range', FIF.PEOPLE, '他人的放贷标准', selectable=False, position=scroll_pos)

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)
        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='user_avatar',
            widget=NavigationAvatarWidget(User.cur_name, User.getAvatarPath()),
            onClick=self.showMsgBox,
            position=NavigationItemPosition.BOTTOM
        )

    def initWindow(self):
        # self.resize(1180, 760)
        self.setFixedSize(1180, 760)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(FIF.IOT.icon()))
        self.setWindowTitle('基于零知识证明的征信评估平台')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()
    
    def showMsgBox(self):
        # change to relog in
        name = User.cur_name
        email = User.getEmail()
        w = MessageBox(
            '当前用户:',
            f'name: {name}\nemail: {email}',
            self
        )
        w.yesButton.setText('重新登录')
        w.cancelButton.setText('返回')
        if w.exec():
            self.loginWindow.show()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.splashScreen.resize(self.size())
    
    def _login(self, success, err):
        if success:
            self._change_avatar(User.cur_name, User.getAvatarPath())
            self.switchTo(self.homeInterface)
            # remove all range and proof interface:
            # myWidget = self.navigationInterface.widget('range')
            # navPanelLayout = myWidget.parent().layout()
            # navPanelLayout.removeWidget(myWidget)
            self.navigationInterface.addItem('range', FIF.PEOPLE, '他人的放贷标准', selectable=False, position=NavigationItemPosition.SCROLL)
        else:
            infoBox = MessageBox('Error:', err, self)
            infoBox.yesButton.setText('重新登录')
            infoBox.cancelButton.setText('返回')
            if infoBox.exec():
                self.loginWindow.show()

    def _exit(self):
        self._change_avatar(User.cur_name, User.getAvatarPath())
        # remove all range and proof interface:

    def _change_avatar(self, name, avatar_path):
        navig= self.navigationInterface
        navig.removeWidget('user_avatar')
        navig.addWidget(
            routeKey='user_avatar',
            widget=NavigationAvatarWidget(name, avatar_path),
            onClick=self.showMsgBox,
            position=NavigationItemPosition.BOTTOM
        )
    
    def _addRangeInterface(self, src_name):
        ranges = User.getUserRanges(src_name)
        routeKey = src_name+'RangePage'
        new_page = RangeInterface(routeKey, ranges, self)
        self.rangePages.append(new_page)
        self.addSubInterface(new_page, FIF.DOCUMENT, f'from {src_name}', parent=self.navigationInterface.widget('range'))

        self.switchTo(new_page)
    

class LoginMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Exit and Re-LogIn', self)
        self.userNameLineEdit = LineEdit(self)
        self.passwdLineEdit = LineEdit(self)
        self.banner = QPixmap(':/my_app/images/login.png')

        self.userNameLineEdit.setPlaceholderText('User Name')
        self.userNameLineEdit.setClearButtonEnabled(True)
        self.passwdLineEdit.setPlaceholderText('Password')
        self.passwdLineEdit.setClearButtonEnabled(True)
        self.passwdLineEdit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        # add widget to view layout
        self.viewLayout.setSpacing(20)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.userNameLineEdit)
        self.viewLayout.addWidget(self.passwdLineEdit)

        # change the text of button
        self.yesButton.setText('Login')
        self.cancelButton.setText('Exit')

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True) # for valid check
        self.passwdLineEdit.textChanged.connect(self._validInput)
        self.yesButton.clicked.connect(self._login)
        self.cancelButton.clicked.connect(self._exit)

    def _validInput(self, text):
        '''check if user input the valid username or passwd'''
        if self.userNameLineEdit.text() and self.passwdLineEdit.text():
            self.yesButton.setEnabled(True)
    
    def _login(self):
        username = self.userNameLineEdit.text()
        passwd = self.passwdLineEdit.text()
        self.userNameLineEdit.clear()
        self.passwdLineEdit.clear()
        User.login(username, passwd)
    
    def _exit(self):
        User.exit()
    
    def paintEvent(self, event):
        # paint the background
        painter = QPainter(self)
        # 获取窗口的尺寸
        window_width = self.width()
        window_height = self.height()
        # 使用 QPixmap 的 scaled 方法缩放图像以适应窗口大小
        scaled_pixmap = self.banner.scaled(window_width, window_height, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        # 计算图像的起始点，确保它居中
        x = (window_width - scaled_pixmap.width()) // 2
        y = (window_height - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)