# coding:utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QEvent
from PyQt6.QtGui import QDesktopServices, QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter, 
                            TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel, toggleTheme)
from ..common.config import cfg, FEEDBACK_URL, HELP_URL, EXAMPLE_URL
from ..common.icon import Icon
from ..common.style_sheet import StyleSheet
from ..backend.signal_bus import signalBus


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

        self.documentButton = PushButton(
            self.tr('Documentation'), self, FluentIcon.DOCUMENT)
        self.sourceButton = PushButton(self.tr('Source'), self, FluentIcon.GITHUB)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)
        self.separator = SeparatorWidget(self)
        self.deleteButton = ToolButton(FluentIcon.DELETE, self)
        self.refreshButton = ToolButton(FluentIcon.SYNC, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(138)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.documentButton, 0, Qt.AlignmentFlag.AlignLeft)
        self.buttonLayout.addWidget(self.sourceButton, 0, Qt.AlignmentFlag.AlignLeft)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.themeButton, 0, Qt.AlignmentFlag.AlignRight)
        self.buttonLayout.addWidget(self.separator, 0, Qt.AlignmentFlag.AlignRight)
        self.buttonLayout.addWidget(self.deleteButton, 0, Qt.AlignmentFlag.AlignRight)
        self.buttonLayout.addWidget(self.refreshButton, 0, Qt.AlignmentFlag.AlignRight)
        self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        self.deleteButton.installEventFilter(ToolTipFilter(self.deleteButton))
        self.refreshButton.installEventFilter(
            ToolTipFilter(self.refreshButton))
        self.themeButton.setToolTip('换主题')
        self.deleteButton.setToolTip('清空')
        self.refreshButton.setToolTip('刷新')

        self.themeButton.clicked.connect(lambda: toggleTheme(True))
        self.deleteButton.clicked.connect(signalBus.supportSignal)




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


class GalleryInterface(ScrollArea):
    """ Gallery interface """

    def __init__(self, title: str, subtitle: str, parent=None):
        """
        Parameters
        ----------
        title: str
            The title of gallery

        subtitle: str
            The subtitle of gallery

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar(title, subtitle, self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName('view')
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
