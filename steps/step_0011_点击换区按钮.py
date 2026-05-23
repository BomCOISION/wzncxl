from __future__ import annotations

from config import CHANGE_SERVER_BUTTON_POINT, CHANGE_SERVER_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(CHANGE_SERVER_BUTTON_WAIT_SECONDS)
    tap_change_server_button(get_context_device())


def tap_change_server_button(serial: str) -> None:
    x, y = CHANGE_SERVER_BUTTON_POINT
    tap_point(serial, int(x), int(y), "换区按钮")
