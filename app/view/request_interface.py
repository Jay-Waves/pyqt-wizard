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
from ..backend.user_manager import User, RangeItem
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

        self.card = CardWidget()
        self.cardLayout = QHBoxLayout(self.card)
        self.addButton = PushButton('Add', self.card, FluentIcon.ADD)
        self.editButton = PushButton('Edit', self.card, FluentIcon.EDIT)
        self.deleteButton = PushButton('Delete', self.card, FluentIcon.DELETE)
        self.infoButton = PushButton('Info', self.card, FluentIcon.INFO)
        self.shareButton = PushButton('Share', self.card, FluentIcon.SHARE)
        self.saveButton = PushButton('Save', self.card, FluentIcon.SAVE)
        self.proofButton = PushButton('Proof', self.card, FluentIcon.FINGERPRINT)
        self.separator = SeparatorWidget(self.card)

        self.stateTooltip = None
        self.progressBar = IndeterminateProgressBar(self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(180)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.card, 1)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.progressBar, 1)
        self.vBoxLayout.setAlignment(AF.AlignTop)

        self.card.setFixedHeight(55)
        # self.cardLayout.setSpacing(20)
        self.cardLayout.setSpacing(15)
        self.cardLayout.setContentsMargins(15, 0, 10, 0)
        self.cardLayout.addWidget(self.addButton, 0, AF.AlignLeft)
        self.cardLayout.addWidget(self.editButton, 0, AF.AlignLeft)
        self.cardLayout.addWidget(self.deleteButton, 0, AF.AlignLeft)
        self.cardLayout.addWidget(self.infoButton, 0, AF.AlignLeft)
        self.cardLayout.addStretch(1)
        self.cardLayout.addWidget(self.separator, 0, AF.AlignRight)
        self.cardLayout.addWidget(self.shareButton, 0, AF.AlignLeft)
        self.cardLayout.addWidget(self.proofButton, 0, AF.AlignLeft)
        self.cardLayout.addWidget(self.saveButton, 0, AF.AlignLeft)
        self.cardLayout.setAlignment(AF.AlignVCenter | AF.AlignLeft)


        # self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        # self.proofButton.setToolTip(self.tr('send request for zk proof'))

        # action triggered
        self.addButton.clicked.connect(self.onAdd)
        self.editButton.clicked.connect(self.onEdit)
        self.progressBar.hide()
        self.proofButton.clicked.connect(self.onProof)

        # experiment
        self.cnt = 0
    
    def onAdd(self):
        print('add clicked')

    def onEdit(self):
        print('edit clicked')

    def onProof(self):
        self.progressBar.show()
        self.stateTooltip = StateToolTip(
            '证明中...', '请在日志界面查看详细输出', self.window())
        # self.sender().setText('Proofing')
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()
        QTimer.singleShot(3000, self._hideTips) # after fixed time, hide the status info flyout

        # if not User.isDefaultUser():
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

class ExampleCard(QWidget):
    """ Example card """

    def __init__(self, title, widget: QWidget, sourcePath, stretch=0, parent=None):
        super().__init__(parent=parent)
        self.widget = widget
        self.stretch = stretch

        self.titleLabel = StrongBodyLabel(title, self)
        self.card = QFrame(self)

        self.sourceWidget = QFrame(self.card)
        self.sourcePath = sourcePath
        self.sourcePathLabel = BodyLabel(
            self.tr('Source code'), self.sourceWidget)
        self.linkIcon = IconWidget(FluentIcon.LINK, self.sourceWidget)

        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout(self.sourceWidget)

        self.__initWidget()

    def __initWidget(self):
        self.linkIcon.setFixedSize(16, 16)
        self.__initLayout()

        self.sourceWidget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sourceWidget.installEventFilter(self)

        self.card.setObjectName('card')
        self.sourceWidget.setObjectName('sourceWidget')

    def __initLayout(self):
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        self.cardLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        self.topLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(12, 12, 12, 12)
        self.bottomLayout.setContentsMargins(18, 18, 18, 18)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.card, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cardLayout.addLayout(self.topLayout, 0)
        self.cardLayout.addWidget(self.sourceWidget, 0, Qt.AlignmentFlag.AlignBottom)

        self.widget.setParent(self.card)
        self.topLayout.addWidget(self.widget)
        if self.stretch == 0:
            self.topLayout.addStretch(1)

        self.widget.show()

        self.bottomLayout.addWidget(self.sourcePathLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.linkIcon, 0, Qt.AlignmentFlag.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    def eventFilter(self, obj, e):
        if obj is self.sourceWidget:
            if e.type() == QEvent.Type.MouseButtonRelease:
                QDesktopServices.openUrl(QUrl(self.sourcePath))

        return super().eventFilter(obj, e)


class RequestInterface(ScrollArea):
    """ Gallery interface """

    def __init__(self, name, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar('制定与交换征信评估标准', "自定义您认可的征信评估标准，并公开。其他用户可以获取并向您证明他们符合资质。", self)
        self.iconView = RangesCardView(User.range, self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 20)
        self.vBoxLayout.addWidget(self.iconView)

        # qss
        self.view.setObjectName('view')
        self.setObjectName('RequestInterface')
        StyleSheet.GALLERY_INTERFACE.apply(self)


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

