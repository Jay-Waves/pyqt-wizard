# coding:utf-8
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTableWidgetItem

from ..common.style_sheet import StyleSheet
from ..backend.signal_bus import signalBus
from ..backend.user_manager import User

from qfluentwidgets import (IconWidget, TextWrap, FlowLayout, CardWidget, 
                            AvatarWidget, BodyLabel, CaptionLabel, HyperlinkButton,
                            setFont, FlyoutView, PushButton, Flyout, FlyoutAnimationType, 
                            FluentIcon, TextWrap, SingleDirectionScrollArea, TableView, TitleLabel, TableWidget)

# LinkCard, on the top
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

# Profile Card
class CustomFlyoutView(FlyoutView):

    def __init__(self, *args, **kwargs):
        self.avatar_width =  45 
        super().__init__(*args, **kwargs)
        # flyoutview
        # add button to view
        button = PushButton('索要其评估标准')
        button.setFixedWidth(180)
        button.clicked.connect(self._addRangeInterface)
        self.addWidget(button, align=Qt.AlignmentFlag.AlignRight)

    def _adjustText(self):
        self.titleLabel.setWordWrap(True)
        # self.contentLabel.setWordWrap(True)
        self.contentLabel.setText(TextWrap.wrap(self.content, self.avatar_width, False)[0])
    
    def _addRangeInterface(self):
        signalBus.newRangeInterface.emit(self.title)
        self.parent().close()



class ProfileCard(CardWidget):
    """ Profile Card """

    def __init__(self, avatarPath, name, email, parent=None):
        super().__init__(parent=parent)
        # self.index = index
        # self.routekey = routeKey
        self.username = name
        self.email = email
        self.avatarPath = avatarPath

        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = QLabel(name, self)
        self.emailLabel = QLabel(TextWrap.wrap(email, 40, False)[0], self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedSize(330, 90)
        # self.iconWidget.setFixedSize(48, 48)
        self.avatar.setRadius(24)
        # self.avatar.move(2, 6)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(self.avatar)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.nameLabel)
        self.vBoxLayout.addWidget(self.emailLabel)
        self.vBoxLayout.addStretch(1)

        self.flyoutView = CustomFlyoutView(
            icon=FluentIcon.PEOPLE, 
            title=name, 
            content=email,
            image=avatarPath)

        # for qss applied
        self.nameLabel.setObjectName('titleLabel')
        self.emailLabel.setObjectName('contentLabel')
        # setFont(self.logoutButton, 13)

    def mouseReleaseEvent(self, e):
        Flyout.make(
            self.flyoutView, self, self.window(), 
            FlyoutAnimationType.SLIDE_RIGHT, 
            isDeleteOnClose=False)



#Info Card
class InfoCard(CardWidget):
    """ personal information card """

    def __init__(self, name, email, parent=None):
        super().__init__(parent=parent)
        # self.index = index
        # self.routekey = routeKey
        self.username = name
        self.email = email
        # check username in database to gain data

        self.titleLabel = TitleLabel('您的个人征信报告', self)
        self.summaryLabel = QLabel(TextWrap.wrap('省流: 您的征信评级为 A 级，信誉良好。', 50, False)[0], self)

        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedSize(330, 90)

        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.summaryLabel)
        self.vBoxLayout.addStretch(1)

        # table flyout view
        self.flyout = FlyoutView(title= '您的个人征信报告', content='')
        table = TableFrame(self.flyout)
        self.flyout.addWidget(table, align=Qt.AlignmentFlag.AlignCenter)
            

        # for qss applied
        self.titleLabel.setObjectName('titleLabel')
        self.summaryLabel.setObjectName('contentLabel')
        # setFont(self.logoutButton, 13)

    def mouseReleaseEvent(self, e):
        # mouse clicked to jump, you should add a flyout to show detailed information
        Flyout.make(self.flyout, self, self.window(), FlyoutAnimationType.SLIDE_RIGHT, isDeleteOnClose=False)


class TableFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)
        StyleSheet.VIEW_INTERFACE.apply(self)

        self.table = TableWidget(self)
        self.hBoxLayout.addWidget(self.table)

        self.table.verticalHeader().hide()
        column_cnt = 4
        self.table.setColumnCount(column_cnt)
        self.table.setRowCount(40)
        self.table.setHorizontalHeaderLabels([
            '名称', '分类', '介绍', '评估值'
        ])


        infos = [
            ['近6月平均收入', '金融资产', '收入',  '50000美元'],
            ['纳税', '金融资产', '近6月平均纳税水平', '2000美元' ],
            ['不动产资产', '实物资产', '房产(住宅), 土地', 'N/A' ],
            ['物品资产', '实物资产', '交通工具(车辆), 珠宝, 艺术品等', '13200美元'],
            ['银行存款', '金融资产', '银行定期存款与存折资产', 'N/A' ],
            ['现金', '金融资产', '属于金融资产',  '8000美元' ],
            ['投资资产', '金融资产', '所拥有债券, 资金, 股票额度', 'N/A' ],
            ['数字资产', '数字资产', '加密货币, 数字藏品',  '4.5444449BTC' ],
            ['保险资产', '保险资产', '人寿保险, 意外伤害保险, 健康保险等', '4200美元'],
            ['呆账数', '征信指标', '持有银行坏账总数',  '0'],
            ['担保', '征信指标', '已承担的担保金额', '0' ],
            ['循坏贷逾期账户数', '征信指标', '持有的信用卡逾期的账户总数',  '2'],
            ['循环贷逾期最大数额', '征信指标', '持有的信用卡逾期的金额总数', '4200美元'],
            ['贷记卡逾期账户数', '征信指标', '持有借记卡逾期的账户总数',  '0'],
            ['贷记卡最大连续逾期月数', '征信指标', '持有借记卡逾期的最长连续月数', '0'],
            ['非循环贷逾期账户数', '征信指标', '持有的单笔贷款逾期总数', '0'],
            ['非循环贷逾期最大数额', '征信指标', '持有的单笔贷款的最大逾期额度', '0'],
            ['正在借款的金融机构数', '偿债能力', '正持有的贷款涉及的金融机构总数','2'],
            ['正在借款的总金额', '偿债能力', '正持有的贷款涉及的金额总数', '1000美元']
        ]

        infos += infos
        for i, info in enumerate(infos):
            for j in range(column_cnt):
                self.table.setItem(i, j, QTableWidgetItem(info[j]))

        self.setFixedSize(650, 440)
        self.table.resizeColumnsToContents()


class SampleCard(CardWidget):
    """ Sample card """

    def __init__(self, icon, title, content, routeKey, index, parent=None):
        super().__init__(parent=parent)
        self.index = index
        self.routekey = routeKey

        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 40, False)[0], self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedSize(330, 90)
        self.iconWidget.setFixedSize(48, 48)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        signalBus.switchToSampleCard.emit(self.routekey, self.index)


class SampleCardView(QWidget):
    """ Sample card view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName('viewTitleLabel')
        StyleSheet.SAMPLE_CARD.apply(self)

    def addSampleCard(self, icon, title, content, routeKey, index):
        """ add sample card """
        card = SampleCard(icon, title, content, routeKey, index, self)
        self.flowLayout.addWidget(card)
    
    def addProfileCard(self, avatarPath, username, email ):
        profile = ProfileCard(avatarPath, username, email, self)
        self.profileCard = profile
        profile.setObjectName('UserProfileCard')
        self.flowLayout.addWidget(profile)

    def addInfoCard(self, username, email):
        infoCard = InfoCard(username, email, self)
        self.infoCard = infoCard
        infoCard.setObjectName('UserInfoCard')
        self.flowLayout.addWidget(infoCard)
    
    def updateUserProfile(self):
        self.profileCard.hide()
        self.infoCard.hide()
        self.addInfoCard(User.cur_name, User.getEmail())
        self.addProfileCard(User.getAvatarPath(), User.cur_name, User.getEmail())

