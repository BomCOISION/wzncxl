from __future__ import annotations

from config import LOGIN_EXIT_BUTTON_POINT, LOGIN_NOTICE_CLOSE_BUTTON_POINT
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds

def run() -> None:
    serial = get_context_device()
    wait_seconds(2)
    tap_login_notice_close_button(serial)
    wait_seconds(2)
    tap_login_exit_button(serial)


def tap_login_notice_close_button(serial: str) -> None:
    x, y = LOGIN_NOTICE_CLOSE_BUTTON_POINT
    tap_point(serial, int(x), int(y), "登录页公告关闭按钮")


def tap_login_exit_button(serial: str) -> None:
    x, y = LOGIN_EXIT_BUTTON_POINT
    tap_point(serial, int(x), int(y), "登录页退出按钮")
