from __future__ import annotations

from config import SETTINGS_LOGOUT_BUTTON_POINT, SETTINGS_LOGOUT_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(SETTINGS_LOGOUT_BUTTON_WAIT_SECONDS)
    tap_settings_logout_button(get_context_device())


def tap_settings_logout_button(serial: str) -> None:
    x, y = SETTINGS_LOGOUT_BUTTON_POINT
    tap_point(serial, int(x), int(y), "设置页退出登录按钮")
