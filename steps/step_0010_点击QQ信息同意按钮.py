from __future__ import annotations

from config import QQ_INFO_AGREE_BUTTON_POINT, QQ_INFO_AGREE_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(QQ_INFO_AGREE_BUTTON_WAIT_SECONDS)
    tap_qq_info_agree_button(get_context_device())


def tap_qq_info_agree_button(serial: str) -> None:
    x, y = QQ_INFO_AGREE_BUTTON_POINT
    tap_point(serial, int(x), int(y), "QQ 信息页同意按钮")
