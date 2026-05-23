from __future__ import annotations

from config import LOGOUT_CONFIRM_BUTTON_POINT, LOGOUT_CONFIRM_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(LOGOUT_CONFIRM_BUTTON_WAIT_SECONDS)
    tap_logout_confirm_button(get_context_device())


def tap_logout_confirm_button(serial: str) -> None:
    x, y = LOGOUT_CONFIRM_BUTTON_POINT
    tap_point(serial, int(x), int(y), "确认退出按钮")
