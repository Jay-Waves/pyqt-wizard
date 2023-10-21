from .request_base_interface import GalleryInterface
from ..backend.user_manager import User
from ..components.ranges_cardview import RangesCardView


class RangeInterface(GalleryInterface):
    """ Icon interface """

    def __init__(self, name, ranges: list, parent=None):
        '''
        ranges: someone's range 
        '''
        super().__init__(
            title='评估申请',
            subtitle="自定义征信评估指标, 并请求第三方证明",
            parent=parent
        )
        self.setObjectName(name)

        self.iconView = RangesCardView(ranges, self)
        self.vBoxLayout.addWidget(self.iconView)
