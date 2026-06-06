from __future__ import annotations

from config import QQ_SWITCH_ACCOUNT_BUTTON_POINT
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(5)
    tap_qq_switch_account_button(get_context_device())


def tap_qq_switch_account_button(serial: str) -> None:
    x, y = QQ_SWITCH_ACCOUNT_BUTTON_POINT
    tap_point(serial, int(x), int(y), "QQ 授权页切换账号按钮")
