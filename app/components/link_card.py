# coding:utf-8
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout

from qfluentwidgets import IconWidget, FluentIcon, TextWrap, SingleDirectionScrollArea
from ..common.style_sheet import StyleSheet


class LinkCard(QFrame):

    def __init__(self, icon, title, content, url=None, parent=None):
        super().__init__(parent=parent)
        if url!=None:
            self.url = QUrl(url)
        else:
            self.url = None
        self.setFixedSize(250, 246)
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 32, False)[0], self)
        self.urlWidget = IconWidget(FluentIcon.LINK, self)

        self.__initWidget()

    def __initWidget(self):
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.iconWidget.setFixedSize(60, 60)
        self.urlWidget.setFixedSize(16, 16)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(24, 24, 0, 13)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(22)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(10)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.urlWidget.move(220, 210)
        if self.url == None:
            self.urlWidget.hide()

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if self.url!=None:
            QDesktopServices.openUrl(self.url)
    

class LinkCardView(SingleDirectionScrollArea):
    """ Link card view """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Orientation.Horizontal)
        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)

        self.hBoxLayout.setContentsMargins(36, 0, 0, 0)
        self.hBoxLayout.setSpacing(20)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.view.setObjectName('view')
        StyleSheet.LINK_CARD.apply(self)

    def addCard(self, icon, title, content, url=None):
        """ add link card """
        card = LinkCard(icon, title, content, url, self.view)
        self.hBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignLeft)
        return card
