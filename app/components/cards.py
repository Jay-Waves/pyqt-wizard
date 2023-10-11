# coding:utf-8
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTableWidgetItem

from ..common.style_sheet import StyleSheet
from ..common.signal_bus import signalBus
from ..common.user_manager import User

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
        button = PushButton('向他借钱!')
        button.setFixedWidth(120)
        self.addWidget(button, align=Qt.AlignmentFlag.AlignRight)

    def _adjustText(self):
        self.titleLabel.setWordWrap(True)
        # self.contentLabel.setWordWrap(True)
        self.contentLabel.setText(TextWrap.wrap(self.content, self.avatar_width, False)[0])


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

        padding = '''veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee 
            eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
            eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
            eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
            eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
            eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
            eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
            eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeery'''
        self.flyout = CustomFlyoutView(
            icon=FluentIcon.PEOPLE, 
            title=name, 
            content=email,
            image=avatarPath)

        # for qss applied
        self.nameLabel.setObjectName('titleLabel')
        self.emailLabel.setObjectName('contentLabel')
        # setFont(self.logoutButton, 13)

    def mouseReleaseEvent(self, e):
        # mouse clicked to jump, you should add a flyout to show detailed information
        Flyout.make(self.flyout, self, self.window(), FlyoutAnimationType.SLIDE_RIGHT, isDeleteOnClose=False)


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
        self.summaryLabel = QLabel(TextWrap.wrap('summary: xxxxxxxxxxxxxxxxxxxxx', 50, False)[0], self)

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
        self.table.setColumnCount(5)
        self.table.setRowCount(60)
        self.table.setHorizontalHeaderLabels([
            'Title', 'Artist', 'Album',
            'Year', 'Duration'
        ])

        songInfos = [
            ['かばん', 'aiko', 'かばん', '2004', '5:04'],
            ['爱你', '王心凌', '爱你', '2004', '3:39'],
            ['星のない世界', 'aiko', '星のない世界/横顔', '2007', '5:30'],
            ['横顔', 'aiko', '星のない世界/横顔', '2007', '5:06'],
            ['秘密', 'aiko', '秘密', '2008', '6:27'],
            ['シアワセ', 'aiko', '秘密', '2008', '5:25'],
            ['二人', 'aiko', '二人', '2008', '5:00'],
            ['スパークル', 'RADWIMPS', '君の名は。', '2016', '8:54'],
            ['なんでもないや', 'RADWIMPS', '君の名は。', '2016', '3:16'],
            ['前前前世', 'RADWIMPS', '人間開花', '2016', '4:35'],
            ['恋をしたのは', 'aiko', '恋をしたのは', '2016', '6:02'],
            ['夏バテ', 'aiko', '恋をしたのは', '2016', '4:41'],
            ['もっと', 'aiko', 'もっと', '2016', '4:50'],
            ['問題集', 'aiko', 'もっと', '2016', '4:18'],
            ['半袖', 'aiko', 'もっと', '2016', '5:50'],
            ['ひねくれ', '鎖那', 'Hush a by little girl', '2017', '3:54'],
            ['シュテルン', '鎖那', 'Hush a by little girl', '2017', '3:16'],
            ['愛は勝手', 'aiko', '湿った夏の始まり', '2018', '5:31'],
            ['ドライブモード', 'aiko', '湿った夏の始まり', '2018', '3:37'],
            ['うん。', 'aiko', '湿った夏の始まり', '2018', '5:48'],
            ['キラキラ', 'aikoの詩。', '2019', '5:08', 'aiko'],
            ['恋のスーパーボール', 'aiko', 'aikoの詩。', '2019', '4:31'],
            ['磁石', 'aiko', 'どうしたって伝えられないから', '2021', '4:24'],
            ['食べた愛', 'aiko', '食べた愛/あたしたち', '2021', '5:17'],
            ['列車', 'aiko', '食べた愛/あたしたち', '2021', '4:18'],
            ['花の塔', 'さユり', '花の塔', '2022', '4:35'],
            ['夏恋のライフ', 'aiko', '夏恋のライフ', '2022', '5:03'],
            ['あかときリロード', 'aiko', 'あかときリロード', '2023', '4:04'],
            ['荒れた唇は恋を失くす', 'aiko', '今の二人をお互いが見てる', '2023', '4:07'],
            ['ワンツースリー', 'aiko', '今の二人をお互いが見てる', '2023', '4:47'],
        ]
        songInfos += songInfos
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(songInfo[j]))

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

