# coding:utf-8
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import (ScrollArea, isDarkTheme, FluentIcon, AvatarWidget, BodyLabel, CaptionLabel, 
                            HyperlinkButton, setFont, TitleLabel)
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.cards import SampleCardView, ProfileCard, LinkCardView
from ..common.style_sheet import StyleSheet
from ..common import resource
from ..common.signal_bus import signalBus
from ..common.user_manager import User


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = TitleLabel('基于零知识范围证明的征信评估平台', self)
        self.banner = QPixmap(':/gallery/images/header1.png')
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignmentFlag.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.linkCardView.addCard(
            # ':/gallery/images/logo.png',
            ':/my_app/images/zk.png', 
            self.tr('密码学新技术'),
            self.tr('基于杂凑函数的新型零知识范围证明，更小的证明体积，支持任意基底，支持批处理。')
        )

        self.linkCardView.addCard(
            FluentIcon.CERTIFICATE,
            self.tr('征信评估新方案'),
            self.tr(
                '使用零知识范围证明，最大限度保护您的个人隐私，同时获取关于您的个人征信报告的可信证明。该证明可作为有效电子凭证，发送给金融机构验证。')
        )

        self.linkCardView.addCard(
            FluentIcon.GITHUB,
            self.tr('高效代码实现'),
            self.tr(
                '核心部分 C++ 实现，使用 BLAKE3 算法计算杂凑值，使用 FFT 算法计算多项式估值。前端 QT 实现。')
        )

        self.linkCardView.addCard(
            FluentIcon.FEEDBACK,
            self.tr('现在开始'),
            self.tr('您可以在首页简要浏览个人征信报告，然后获取关于它的零知识证明，详细操作手册见文档。如果有任何问题，请反馈给我们，谢谢。'),
            FEEDBACK_URL
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
        w, h = self.width(), 200
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h-50, 50, 50))
        path.addRect(QRectF(w-50, 0, 50, 50))
        path.addRect(QRectF(w-50, h-50, 50, 50))
        path = path.simplified()

        # draw background color
        if not isDarkTheme():
            painter.fillPath(path, QColor(206, 216, 228))
        else:
            painter.fillPath(path, QColor(0, 0, 0))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        path.addRect(QRectF(0, h, w, self.height() - h))
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

        # signals
        User.userLogin.connect(self._login)
        User.userExit.connect(self._exit)

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(25)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def loadSamples(self):
        """ load samples """

        self.selfInfoView = SampleCardView("这是您:", self.view)
        # note that infocard and profilecard's parent is home interface
        self.selfInfoView.addInfoCard(User.cur_name, 'swt@buaa.edu.cn')
        self.selfInfoView.addProfileCard(User.getAvatarPath(), User.cur_name, User.getEmail())
        self.vBoxLayout.addWidget(self.selfInfoView)


        basicInputView = SampleCardView("您的朋友们:", self.view)
        basicInputView.addProfileCard(':/my_app/images/users/luminous.png', 'YJW', 'yujiawei@buaa.edu.cn')
        basicInputView.addProfileCard(':/my_app/images/users/bill_gates.png', 'Bill Gates', 'Intel giveth, I takenth away')
        basicInputView.addProfileCard(':/my_app/images/users/musk.png', 'Elon Musk', 'You are fired')
        basicInputView.addProfileCard(':/my_app/images/users/guido_van_rossum.png', 'Guido van Rossum', 'Python is the best language')
        basicInputView.addProfileCard(':/my_app/images/users/richard_stallman.png', 'Richard Stallman', 'I will find you, and GPL you')
        basicInputView.addProfileCard(':/my_app/images/users/jeffrey_preston.png', 'Jeffrey Preston', 'jp')
        basicInputView.addProfileCard(':/my_app/images/users/tim_berners_lee.png', 'Tim Berners-Lee', 'tbl')
        basicInputView.addProfileCard(':/my_app/images/users/nvidia.png', 'Linus Torvalds', 'Fuck You! Nvidia!')
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Button.png",
            title="Button",
            content=self.tr(
                "A control that responds to user input and emit clicked signal."),
            routeKey="basicInputInterface",
            index=0
        )
        self.vBoxLayout.addWidget(basicInputView)

        basicInputView = SampleCardView(
            self.tr("金融机构:"), self.view)
        basicInputView.addProfileCard(':/my_app/images/users/luminous.png', 'YJW', 'yujiawei@buaa.edu.cn')
        basicInputView.addProfileCard(':/my_app/images/users/bill_gates.png', 'Bill Gates', 'Intel giveth, I takenth away')
        basicInputView.addProfileCard(':/my_app/images/users/musk.png', 'Elon Musk', 'You are fired')
        basicInputView.addProfileCard(':/my_app/images/users/guido_van_rossum.png', 'Guido van Rossum', 'Python is the best language')
        basicInputView.addProfileCard(':/my_app/images/users/richard_stallman.png', 'Richard Stallman', 'I will find you, and GPL you')
        basicInputView.addProfileCard(':/my_app/images/users/jeffrey_preston.png', 'Jeffrey Preston', 'jp')
        basicInputView.addProfileCard(':/my_app/images/users/tim_berners_lee.png', 'Tim Berners-Lee', 'tbl')
        basicInputView.addProfileCard(':/my_app/images/users/nvidia.png', 'Linus Torvalds', 'Fuck You! Nvidia!')
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Button.png",
            title="Button",
            content=self.tr(
                "A control that responds to user input and emit clicked signal."),
            routeKey="basicInputInterface",
            index=0
        )
        self.vBoxLayout.addWidget(basicInputView)
        # add workflow image after that
    
    def _login(self, success, err):
        if success:
            self.selfInfoView.updateUserProfile()

    def _exit(self):
        self.selfInfoView.updateUserProfile()