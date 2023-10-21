
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QEvent, QTimer
from PyQt6.QtGui import QDesktopServices, QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter, TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel, toggleTheme, CommandBar, Action, CardWidget,
                            IndeterminateProgressBar, StateToolTip, InfoBarPosition, InfoBar, InfoBarIcon)
from ..common.config import cfg, FEEDBACK_URL, HELP_URL, EXAMPLE_URL
from ..common.icon import Icon
from ..common.style_sheet import StyleSheet
from ..backend.signal_bus import signalBus
from ..backend.zkrp import zkrp
from ..backend.user_manager import User
from ..components.profile_cardview import ProfileCard
from ..components.ranges_cardview import RangesCardView

AF = Qt.AlignmentFlag

class SeparatorWidget(QWidget):
    """ Seperator widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(6, 16)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(1)
        pen.setCosmetic(True)
        c = QColor(255, 255, 255, 21) if isDarkTheme() else QColor(0, 0, 0, 15)
        pen.setColor(c)
        painter.setPen(pen)

        x = self.width() // 2
        painter.drawLine(x, 0, x, self.height())


class ToolBar(QWidget):
    """ Tool bar """

    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxWidget = QWidget()
        self.hBoxLayout = QHBoxLayout(self.hBoxWidget)

        self.card = CardWidget()
        self.cardLayout = QHBoxLayout(self.card)
        self.shareButton = PushButton('Share', self.card, FluentIcon.SHARE)
        self.saveButton = PushButton('Save', self.card, FluentIcon.SAVE)
        self.proofButton = PushButton('Proof', self.card, FluentIcon.FINGERPRINT)
        self.separator = SeparatorWidget(self.card)
        self.profileCard = ProfileCard(
            avatarPath=":/my_app/images/users/luminous.png", 
            name="Source: YJW", 
            email="yujiawei@buaa.edu.cn", 
            parent=self
        )
        self.stateTooltip = None
        self.progressBar = IndeterminateProgressBar(self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(220)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(26, 15, 0, 0)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.hBoxWidget, 1)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.progressBar, 1)
        self.vBoxLayout.setAlignment(AF.AlignTop)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.addWidget(self.profileCard, 0, AF.AlignLeft)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.card, 0)
        self.hBoxLayout.addSpacing(30)

        self.card.setFixedHeight(55)
        # self.cardLayout.setSpacing(20)
        self.cardLayout.setSpacing(10)
        self.cardLayout.setContentsMargins(15, 0, 10, 0)
        self.cardLayout.addStretch(1)
        self.cardLayout.addWidget(self.separator)
        self.cardLayout.addWidget(self.shareButton, 0)
        self.cardLayout.addWidget(self.proofButton, 0)
        self.cardLayout.addWidget(self.saveButton, 0)

        # self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        # self.proofButton.setToolTip(self.tr('send request for zk proof'))

        # action triggered
        self.progressBar.hide()
        self.proofButton.clicked.connect(self.onProof)
    
    def onProof(self):
        self.progressBar.show()
        self.stateTooltip = StateToolTip(
            '证明中...', '请在日志界面查看详细输出', self.window())
        self.sender().setText('Proofing')
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()
        QTimer.singleShot(3000, self._hideTips) # after fixed time, hide the status info flyout

        if not User.isDefaultUser():
            zkrp.proving()
    
    def _hideTips(self):
        self.progressBar.hide()
        self.stateTooltip.hide()

        InfoBar.success(
            title='Success',
            content="生成证明成功, 你可以在证明存储界面选择将其分享给其他人",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self
        )


class RangeInterface(ScrollArea):
    """ Gallery interface """

    def __init__(self, name, ranges: list, parent=None):
        """
        Parameters
        ----------
        name: str
            interface name

        ranges: list 
            other user's range
        """
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar('他人的征信评估标准', "您可以查阅后，对其进行证明。", self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(26, 15, 26, 20)

        # apply qss
        self.view.setObjectName('view')
        self.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

        self.iconView = RangesCardView(ranges, self)
        self.vBoxLayout.addWidget(self.iconView)

    def addExampleCard(self, title, widget, sourcePath: str, stretch=0):
        card = ExampleCard(title, widget, sourcePath, stretch, self.view)
        self.vBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignTop)
        return card

    def scrollToCard(self, index: int):
        """ scroll to example card """
        w = self.vBoxLayout.itemAt(index).widget()
        self.verticalScrollBar().setValue(w.y())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())
