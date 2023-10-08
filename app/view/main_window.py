# coding: utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl, QSize
from PyQt6.QtGui import QIcon, QDesktopServices, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget, QLineEdit

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen, setTheme, Theme, MessageBoxBase, SubtitleLabel, LineEdit)
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .basic_input_interface import BasicInputInterface
from .date_time_interface import DateTimeInterface
from .log_interface import LogInterface
from .layout_interface import LayoutInterface
from .request_interface import requestInterface
from .material_interface import MaterialInterface
from .menu_interface import MenuInterface
from .navigation_view_interface import NavigationViewInterface
from .scroll_interface import ScrollInterface
from .status_info_interface import StatusInfoInterface
from .setting_interface import SettingInterface
from .text_interface import TextInterface
from .view_interface import ViewInterface
from ..common.config import SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common import resource
# pyrcc6 -o resource resources.qrc


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.requestInterface = requestInterface(self)
        self.basicInputInterface = BasicInputInterface(self)
        self.dateTimeInterface = DateTimeInterface(self)
        self.logInterface = LogInterface(self)
        self.layoutInterface = LayoutInterface(self)
        # self.menuInterface = MenuInterface(self)
        # self.materialInterface = MaterialInterface(self)
        # self.navigationViewInterface = NavigationViewInterface(self)
        # self.scrollInterface = ScrollInterface(self)
        # self.statusInfoInterface = StatusInfoInterface(self)
        self.settingInterface = SettingInterface(self)
        # self.textInterface = TextInterface(self)
        # self.viewInterface = ViewInterface(self)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.showMsgBox)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('首页'))
        # self.addSubInterface(self.basicInputInterface, FIF.FINGERPRINT,'首页')
        self.addSubInterface(self.requestInterface, FIF.PENCIL_INK, '评估申请')
        self.addSubInterface(self.logInterface, FIF.COMMAND_PROMPT, '日志信息')
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.navigationInterface.addItem('people yjw', FIF.PEOPLE, '评估证书：来自用户 YJW', selectable=False, position=NavigationItemPosition.SCROLL)
        self.addSubInterface(self.dateTimeInterface, FIF.CERTIFICATE, '2023 年 10 月 4 日  04 : 40', parent=self.navigationInterface.widget('people yjw'))
        self.addSubInterface(self.layoutInterface, FIF.CERTIFICATE, '2023 年 10 月 4 日  05 : 30', parent=self.navigationInterface.widget('people yjw'))
        # self.addSubInterface(self.materialInterface, FIF.PALETTE, t.material, pos)
        # self.addSubInterface(self.menuInterface, Icon.MENU, t.menus, pos)
        # self.addSubInterface(self.navigationViewInterface, FIF.MENU, t.navigation, pos)
        # self.addSubInterface(self.scrollInterface, FIF.SCROLL, t.scroll, pos)
        # self.addSubInterface(self.statusInfoInterface, FIF.CHAT, t.statusInfo, pos)
        # self.addSubInterface(self.textInterface, Icon.TEXT, t.text, pos)
        # self.addSubInterface(self.viewInterface, Icon.GRID, t.view, pos)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('SWT', ':/my_app/images/went.png'),
            onClick=self.showMsgBox,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1180, 760)
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
        w = MessageBox(
            '当前用户',
            'SWT \n\n 2291303762@qq.com',
            self
        )
        w.yesButton.setText('重新登录')
        w.cancelButton.setText('返回')
        # w.yesButton.clicked.connect(self.showLoginBox)

        if w.exec():
            loginWindow = LoginMessageBox(self.window())
            loginWindow.exec()
        

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)


class LoginMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr('Exit and Re-LogIn'), self)
        self.userNameLineEdit = LineEdit(self)
        self.passwdLineEdit = LineEdit(self)
        self.banner = QPixmap(':/my_app/images/login.png')

        self.userNameLineEdit.setPlaceholderText(self.tr('User Name'))
        self.userNameLineEdit.setClearButtonEnabled(True)
        self.passwdLineEdit.setPlaceholderText(self.tr('Password'))
        self.passwdLineEdit.setClearButtonEnabled(True)
        self.passwdLineEdit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        # add widget to view layout
        self.viewLayout.setSpacing(20)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.userNameLineEdit)
        self.viewLayout.addWidget(self.passwdLineEdit)

        # change the text of button
        self.yesButton.setText(self.tr('Login'))
        self.cancelButton.setText(self.tr('Exit'))

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True) # for valid check
        self.passwdLineEdit.textChanged.connect(self._validInput)

    def _validInput(self, text):
        '''check if user input the valid username or passwd'''
        if self.userNameLineEdit.text() and self.passwdLineEdit.text():
            self.yesButton.setEnabled(True)
    
    def paintEvent(self, event):
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
    
    def changeUser(self):
        # if login success, remove the avator, add a new one with new user portrait
        # remember to wait for a second, and pop out a state fly tip
        return
    
    def noUserState(self):
        # if login exit, use null portrait
        return