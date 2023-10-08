# coding:utf-8
from typing import List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, ZhDatePicker)

from .request_base_interface import GalleryInterface
from ..common.translator import Translator
from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..common.trie import Trie


class LineEdit(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText('Search Item')
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)


class IconCard(QFrame):
    """ Icon card """

    # 这个改为某种征信评估标准, 如: 循环贷, 贷记卡, 非循环贷, 呆账, 资产证明
    # 旁边栏就放介绍和编辑按钮. 包括调整想要的比重
    clicked = pyqtSignal(FluentIcon)
    def __init__(self, icon: FluentIcon, parent=None):
        super().__init__(parent=parent)
        self.icon = icon
        self.isSelected = False

        self.iconWidget = IconWidget(icon, self)
        self.nameLabel = QLabel(self)
        self.hBoxLayout = QHBoxLayout(self)  # 使用水平布局

        self.setFixedSize(256, 96)
        self.hBoxLayout.setSpacing(14)  # 两个控件之间的空间
        self.hBoxLayout.setContentsMargins(28, 8, 8, 8)  # 调整外边距
        self.iconWidget.setFixedSize(28, 28)
        self.hBoxLayout.addWidget(self.iconWidget)  
        self.hBoxLayout.addWidget(self.nameLabel)  
       
        text = self.nameLabel.fontMetrics().elidedText(icon.value, Qt.TextElideMode.ElideRight, 90)
        self.nameLabel.setText(text)
        # self.nameLabel.setText('hello')

    def mouseReleaseEvent(self, e):
        if self.isSelected:
            return

        self.clicked.emit(self.icon)

    def setSelected(self, isSelected: bool, force=False):
        if isSelected == self.isSelected and not force:
            return

        self.isSelected = isSelected

        if not isSelected:
            self.iconWidget.setIcon(self.icon)
        else:
            icon = self.icon.icon(Theme.LIGHT if isDarkTheme() else Theme.DARK)
            self.iconWidget.setIcon(icon)

        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())


class IconInfoPanel(QFrame):
    """ Icon info panel """

    def __init__(self, icon: FluentIcon, parent=None):
        super().__init__(parent=parent)
        self.nameLabel = QLabel(icon.value, self)
        self.iconWidget = IconWidget(icon, self)
        self.iconNameTitleLabel = QLabel(self.tr('Icon name'), self)
        self.iconNameLabel = QLabel(icon.value, self)
        self.enumNameTitleLabel = QLabel(self.tr('Enum member'), self)
        self.enumNameLabel = QLabel("FluentIcon." + icon.name, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 20, 16, 20)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vBoxLayout.addWidget(self.nameLabel)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(45)
        self.vBoxLayout.addWidget(self.iconNameTitleLabel)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.iconNameLabel)
        self.vBoxLayout.addSpacing(34)
        self.vBoxLayout.addWidget(self.enumNameTitleLabel)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.enumNameLabel)

        self.iconWidget.setFixedSize(48, 48)
        # self.setFixedWidth(280)
        self.setMinimumWidth(380)

        self.nameLabel.setObjectName('nameLabel')
        self.iconNameTitleLabel.setObjectName('subTitleLabel')
        self.enumNameTitleLabel.setObjectName('subTitleLabel')

    def setIcon(self, icon: FluentIcon):
        self.iconWidget.setIcon(icon)
        self.nameLabel.setText(icon.value)
        self.iconNameLabel.setText(icon.value)
        self.enumNameLabel.setText("FluentIcon."+icon.name)


class IconCardView(QWidget):
    """ Icon card view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.trie = Trie()
        self.iconLibraryLabel = StrongBodyLabel(self.tr('征信评估指标仓库'), self)
        self.bar = QWidget(self)
        self.barLayout = QHBoxLayout(self.bar)
        self.searchLineEdit = LineEdit(self.bar)
        self.dataPicker = ZhDatePicker(self.bar)

        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)
        self.infoPanel = IconInfoPanel(FluentIcon.MENU, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.flowLayout = FlowLayout(self.scrollWidget, isTight=True)

        self.cards = []     # type:List[IconCard]
        self.icons = []
        self.currentIndex = -1

        self.__initWidget()

    def __initWidget(self):
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setViewportMargins(5, 10, 0, 5)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.iconLibraryLabel)
        self.vBoxLayout.addWidget(self.bar)
        self.vBoxLayout.addWidget(self.view)

        self.barLayout.setContentsMargins(10, 0, 0, 0)
        self.barLayout.addWidget(self.dataPicker, 0, Qt.AlignmentFlag.AlignLeft)
        self.barLayout.addWidget(self.searchLineEdit, 0, Qt.AlignmentFlag.AlignRight)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.scrollArea)
        self.hBoxLayout.addWidget(self.infoPanel, 0, Qt.AlignmentFlag.AlignRight)

        self.flowLayout.setVerticalSpacing(8)
        self.flowLayout.setHorizontalSpacing(8)
        self.flowLayout.setContentsMargins(8, 3, 8, 8)

        self.__setQss()
        cfg.themeChanged.connect(self.__setQss)
        self.searchLineEdit.clearSignal.connect(self.showAllIcons)
        self.searchLineEdit.searchSignal.connect(self.search)

        for icon in FluentIcon._member_map_.values():
            # change FluentIcon to ours 
            self.addIcon(icon)

        self.setSelectedIcon(self.icons[0])

    def addIcon(self, icon: FluentIcon):
        """ add icon to view """
        card = IconCard(icon, self)
        card.clicked.connect(self.setSelectedIcon)

        self.trie.insert(icon.value, len(self.cards))
        self.cards.append(card)
        self.icons.append(icon)
        self.flowLayout.addWidget(card)

    def setSelectedIcon(self, icon: FluentIcon):
        """ set selected icon """
        index = self.icons.index(icon)

        if self.currentIndex >= 0:
            self.cards[self.currentIndex].setSelected(False)

        self.currentIndex = index
        self.cards[index].setSelected(True)
        self.infoPanel.setIcon(icon)

    def __setQss(self):
        self.view.setObjectName('iconView')
        self.scrollWidget.setObjectName('scrollWidget')

        StyleSheet.ICON_INTERFACE.apply(self)
        StyleSheet.ICON_INTERFACE.apply(self.scrollWidget)

        if self.currentIndex >= 0:
            self.cards[self.currentIndex].setSelected(True, True)

    def search(self, keyWord: str):
        """ search icons """
        items = self.trie.items(keyWord.lower())
        indexes = {i[1] for i in items}
        self.flowLayout.removeAllWidgets()

        for i, card in enumerate(self.cards):
            isVisible = i in indexes
            card.setVisible(isVisible)
            if isVisible:
                self.flowLayout.addWidget(card)

    def showAllIcons(self):
        self.flowLayout.removeAllWidgets()
        for card in self.cards:
            card.show()
            self.flowLayout.addWidget(card)


class requestInterface(GalleryInterface):
    """ Icon interface """

    def __init__(self, parent=None):
        super().__init__(
            title='评估申请',
            subtitle="自定义征信评估指标, 并请求第三方证明",
            parent=parent
        )
        self.setObjectName('iconInterface')

        self.iconView = IconCardView(self)
        self.vBoxLayout.addWidget(self.iconView)
