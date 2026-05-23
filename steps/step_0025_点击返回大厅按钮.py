from __future__ import annotations

from config import BACK_TO_LOBBY_BUTTON_POINT, BACK_TO_LOBBY_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(BACK_TO_LOBBY_BUTTON_WAIT_SECONDS)
    tap_back_to_lobby_button(get_context_device())


def tap_back_to_lobby_button(serial: str) -> None:
    x, y = BACK_TO_LOBBY_BUTTON_POINT
    tap_point(serial, int(x), int(y), "返回大厅按钮")
