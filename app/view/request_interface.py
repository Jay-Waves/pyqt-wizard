from .request_base_interface import GalleryInterface
from ..components.ranges_cardview import RangesCardView
from ..backend.user_manager import User, RangeItem



class RequestInterface(GalleryInterface):
    """ Icon interface """

    def __init__(self, name, parent=None):
        super().__init__(
            title='评估申请',
            subtitle="自定义征信评估指标, 并请求第三方证明",
            parent=parent
        )
        self.setObjectName(name)

        self.iconView = RangesCardView(User.range, self)
        self.vBoxLayout.addWidget(self.iconView)
