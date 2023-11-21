# coding:utf-8
from PyQt6.QtWidgets import (QWidget, QFrame, QHBoxLayout, QVBoxLayout, 
                            QTreeWidgetItem, QTreeWidgetItemIterator)
from PyQt6.QtCore import Qt, QTimer

from qfluentwidgets import (DatePicker, TimePicker, AMTimePicker, 
                            ZhDatePicker, CalendarPicker, ScrollArea, 
                            TreeWidget, InfoBar, InfoBarPosition,
                            FluentIcon, PushButton, TitleLabel, 
                            CaptionLabel, CardWidget, StateToolTip)

from ..common.style_sheet import StyleSheet
from ..components.profile_cardview import TableFrame
from ..backend.zkrp import zkrp

class TreeFrame(QFrame):

    def __init__(self, parent=None, enableCheck=False):
        super().__init__(parent)
        self.tree = TreeWidget(self)
        self.table = TableFrame(self)
        self.menu = None
        title = TitleLabel('验证界面')
        subtitle = CaptionLabel('显示收到的零知识证明，您可以选中一个然后开始验证')
        self.leftFrame = QFrame(self)
        self.card = CardWidget(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.hLayout = QHBoxLayout(self)
        self.vLayout = QVBoxLayout(self.leftFrame)  

        self.cardLayout.setContentsMargins(5, 10, 10, 10)
        self.cardLayout.addWidget(self.tree)

        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.setSpacing(15)
        self.vLayout.addWidget(title)
        self.vLayout.addWidget(subtitle)
        self.vLayout.addWidget(self.card)

        self.hLayout.setContentsMargins(20, 0, 0, 0)
        self.hLayout.addWidget(self.leftFrame)
        self.hLayout.setSpacing(10)
        self.hLayout.addWidget(self.table)

        # set the table widget:
        self.table.setFixedSize(700, 750)

        # set the tree widget:
        self.tree.itemClicked.connect(self.on_item_clicked)
        item1 = QTreeWidgetItem(['您个人征信报告的证明结果'])
        item1.addChildren([
            QTreeWidgetItem(['Jonathan Joestar']),
            QTreeWidgetItem(['Dio Brando']),
            QTreeWidgetItem(['Will A. Zeppeli']),
        ])
        self.tree.addTopLevelItem(item1)

        item2 = QTreeWidgetItem(['受您评估者的征信报告的证明结果'])
        item21 = QTreeWidgetItem(['Jotaro Kujo'])
        item22 = QTreeWidgetItem(['John Mendoes'])
        item23 = QTreeWidgetItem(['swt'])
        '''item21.addChildren([
            QTreeWidgetItem(['空条承太郎']),
            QTreeWidgetItem(['空条蕉太狼']),
            QTreeWidgetItem(['阿强']),
            QTreeWidgetItem(['卖鱼强']),
            QTreeWidgetItem(['那个无敌的男人']),
        ])'''
        item2.addChild(item21)
        item2.addChild(item22)
        item2.addChild(item23)
        self.tree.addTopLevelItem(item2)
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)
        self.setMinimumWidth(300)

        # use to count sum of proofs
        # if enableCheck:
        #     it = QTreeWidgetItemIterator(self.tree)
        #     while it.value():
        #         it.value().setCheckState(0, Qt.CheckState.Unchecked)
        #         it += 1
    
    def on_item_clicked(self, item, column):
        if self.menu == None:
            self.menu = InfoBar(
                        icon=FluentIcon.DEVELOPER_TOOLS,
                        title='工具栏',
                        content='对你选中的证明结果进行操作:  ',
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        duration=-1,
                        position=InfoBarPosition.BOTTOM_LEFT,
                        parent=self
                    )
            # set menu bar
            self.button1 = PushButton('验证')
            self.button1.clicked.connect(self.on_proof)
            self.menu.addWidget(self.button1)
            self.menu.addWidget(PushButton('删除'))
            self.menu.setCustomBackgroundColor("#00ffff", "#2a2a2a")
            # when menu closed, qt will destroy obj, then python holds meaningless ptr
            self.menu.destroyed.connect(lambda: setattr(self, 'menu', None))
            self.menu.show()

    def on_proof(self):
        self.stateTooltip = StateToolTip(
            '验证中...', '请在日志界面查看详细输出', self.window())
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()
        QTimer.singleShot(3000, self._hideTips) # after fixed time, hide the status info flyou
        zkrp.proving()

    def _hideTips(self):
        self.stateTooltip.hide()
        InfoBar.success(
            title='Success',
            content="验证成功，该用户通过您的征信评估",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self
        )

class ProofInterface(QWidget):
    """ Date time interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vLayout = QVBoxLayout(self)

        # set scrollarea
        self.vLayout.setSpacing(20)
        self.vLayout.setContentsMargins(0, 10, 10, 15)
        self.vLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # add widget 
        self.tree = TreeFrame(self)
        self.vLayout.addWidget(self.tree)

        # apply qss
        self.setObjectName('ProofInterface')
        StyleSheet.GALLERY_INTERFACE.apply(self)
