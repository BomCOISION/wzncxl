from __future__ import annotations

from config import QQ_IOS_FRIEND_BUTTON_POINT
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(1)
    tap_qq_ios_friend_button(get_context_device())


def tap_qq_ios_friend_button(serial: str) -> None:
    x, y = QQ_IOS_FRIEND_BUTTON_POINT
    tap_point(serial, int(x), int(y), "QQ 与 iOS 好友玩按钮")
