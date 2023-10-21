# coding:utf-8
from PyQt6.QtWidgets import (QWidget, QFrame, QHBoxLayout, QVBoxLayout, 
                            QTreeWidgetItem, QTreeWidgetItemIterator)
from PyQt6.QtCore import Qt
from qfluentwidgets import (DatePicker, TimePicker, AMTimePicker, 
                            ZhDatePicker, CalendarPicker, ScrollArea, 
                            TreeWidget, InfoBar, InfoBarPosition,
                            FluentIcon, PushButton)

from ..common.style_sheet import StyleSheet
from ..components.profile_cardview import TableFrame

class TreeFrame(QFrame):

    def __init__(self, parent=None, enableCheck=False):
        super().__init__(parent)
        self.tree = TreeWidget(self)
        self.table = TableFrame(self)
        self.menu = None

        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(20, 0, 0, 0)
        self.hLayout.addWidget(self.tree)
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
        item21.addChildren([
            QTreeWidgetItem(['空条承太郎']),
            QTreeWidgetItem(['空条蕉太狼']),
            QTreeWidgetItem(['阿强']),
            QTreeWidgetItem(['卖鱼强']),
            QTreeWidgetItem(['那个无敌的男人']),
        ])
        item2.addChild(item21)
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
            self.menu.addWidget(PushButton('验证'))
            self.menu.addWidget(PushButton('删除'))
            self.menu.setCustomBackgroundColor("white", "#2a2a2a")
            # when menu closed, qt will destroy obj, then python holds meaningless ptr
            self.menu.destroyed.connect(lambda: setattr(self, 'menu', None))
            self.menu.show()


class ProofInterface(QWidget):
    """ Date time interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('ProofInterface')
        self.vLayout = QVBoxLayout(self)

        # set scrollarea
        self.vLayout.setSpacing(20)
        self.vLayout.setContentsMargins(10, 10, 10, 15)
        self.vLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # add widget 
        self.tree = TreeFrame(self)
        self.vLayout.addWidget(self.tree)

        # apply qss
        self.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)
