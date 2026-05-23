from __future__ import annotations

from config import LOGIN_EXIT_BUTTON_POINT
from common.run_context import get_context_device
from common.touch_utils import tap_point


def run() -> None:
    tap_login_exit_button(get_context_device())


def tap_login_exit_button(serial: str) -> None:
    x, y = LOGIN_EXIT_BUTTON_POINT
    tap_point(serial, int(x), int(y), "登录页退出按钮")
