
# coding:utf-8
from typing import List

from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit, StrongBodyLabel,
                            BodyLabel, ZhDatePicker)

from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..common.trie import Trie
from .progress import MyRangeWidget
from ..backend.user_manager import User, RangeItem


class LineEdit(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText('Search Item')
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)


class IconCard(QFrame):
    """ Icon card """
    clicked = pyqtSignal(FluentIcon)
    def __init__(self, item: RangeItem, parent=None):
        super().__init__(parent=parent)
        # info
        self.icon = item.icon
        self.name = item.name
        self.en_name = item.en_name
        self.intro = item.introduction
        self.up = item.up
        self.down = item.down
        self.unit = item.unit

        self.isSelected = False

        self.iconWidget = IconWidget(self.icon, self)
        self.nameLabel = QLabel()
        self.enNameLabel = QLabel()
        self.introLabel = QLabel()
        self.frame = QFrame()
        self.hBoxLayout = QHBoxLayout(self)  # 使用水平布局
        self.vBoxLayout = QVBoxLayout(self.frame)  

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.nameLabel)
        self.vBoxLayout.addWidget(self.enNameLabel)
        self.vBoxLayout.addWidget(self.introLabel)

        self.setFixedSize(256, 96)
        self.hBoxLayout.setSpacing(5)  # 两个控件之间的空间
        self.hBoxLayout.setContentsMargins(10, 5, 8, 8)  # 调整外边距
        self.iconWidget.setFixedSize(28, 28)
        self.hBoxLayout.addWidget(self.iconWidget)  
        self.hBoxLayout.addWidget(self.frame)  
       
        self.nameLabel.setText(self.name)
        self.enNameLabel.setText(self.en_name)
        self.introLabel.setText(self.intro)

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
    
    def update(self, item: RangeItem):
        # different user has different range
        self.up = item.up
        self.dwn = item.down



class IconInfoPanel(QFrame):
    """ Icon info panel """

    def __init__(self, icon: FluentIcon, parent=None):
        super().__init__(parent=parent)
        self.nameLabel = QLabel("place holder", self)
        self.iconWidget = IconWidget(icon, self)
        self.enNameTitle = QLabel('英文名称:', self)
        self.enName = QLabel(icon.value, self)
        self.introTitle = QLabel("介绍:", self)
        self.intro = QLabel("hold placer", self)
        self.rangeTitle = QLabel("hold placer", self)
        self.range = QWidget()

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 20, 16, 20)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vBoxLayout.addWidget(self.nameLabel)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(30)
        self.vBoxLayout.addWidget(self.enNameTitle)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.enName)
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.introTitle)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.intro)
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.rangeTitle)

        self.iconWidget.setFixedSize(48, 48)
        # self.setFixedWidth(280)
        self.setMinimumWidth(380)

        # apply qss
        self.nameLabel.setObjectName('nameLabel')
        self.enNameTitle.setObjectName('subTitleLabel')
        self.introTitle.setObjectName('subTitleLabel')
        self.rangeTitle.setObjectName('subTitleLabel')

    def setInfo(self, card):
        self.iconWidget.setIcon(card.icon)
        self.nameLabel.setText(card.name)
        self.enName.setText(card.en_name)
        self.intro.setText(card.intro)
        self.rangeTitle.setText(f"范围上下限: ({card.unit})")

        self.range.hide()
        self.range = MyRangeWidget(card.down, card.up, card.unit, self)
        self.vBoxLayout.addWidget(self.range)


class RangesCardView(QWidget):
    """ Icon card view """

    def __init__(self, ranges: List, parent=None):
        super().__init__(parent=parent)
        self.trie = Trie()
        self.iconLibraryLabel = StrongBodyLabel('征信评估标准 参考小项', self)
        self.bar = QWidget(self)
        self.barLayout = QHBoxLayout(self.bar)
        self.searchLineEdit = LineEdit(self.bar)
        self.dataPicker = ZhDatePicker(self.bar)
        self.dataPicker.setDate(QDate.currentDate())
        self.dueLabel = QLabel('该标准有效期截至：', self.bar)

        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)
        self.infoPanel = IconInfoPanel(FluentIcon.MENU, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.flowLayout = FlowLayout(self.scrollWidget, isTight=True)

        self.ranges = ranges
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
        self.barLayout.addWidget(self.dueLabel)# Qt.AlignmentFlag.AlignLeft)
        self.barLayout.addWidget(self.dataPicker)
        self.barLayout.addStretch(1)
        self.barLayout.addWidget(self.searchLineEdit)

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
        User.userLogin.connect(self.updateAllIcons)
        self.searchLineEdit.searchSignal.connect(self.search)

        for item in self.ranges:
            self.addItem(RangeItem(item))

        self.setSelectedIcon(self.icons[0])
    
    def addItem(self, item):
        card = IconCard(item, self)
        card.clicked.connect(self.setSelectedIcon)

        self.trie.insert(item.en_name, len(self.cards))
        self.cards.append(card)
        self.icons.append(item.icon)
        self.flowLayout.addWidget(card)

    def setSelectedIcon(self, icon: FluentIcon):
        """ set selected icon """
        index = self.icons.index(icon)

        if self.currentIndex >= 0:
            self.cards[self.currentIndex].setSelected(False)

        self.currentIndex = index
        card = self.cards[index]
        card.setSelected(True)
        self.infoPanel.setInfo(card)

    def __setQss(self):
        self.view.setObjectName('iconView')
        self.scrollWidget.setObjectName('scrollWidget')
        self.dueLabel.setObjectName('dueLabel')

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
    
    def updateAllIcons(self):
        #TODO use the new user information to update card information
        self.flowLayout.removeAllWidgets()
        for card, item in zip(self.cards, self.ranges):
            card.update(RangeItem(item))
            card.show()
            self.flowLayout.addWidget(card)
