from __future__ import annotations

from config import LOBBY_SETTINGS_BUTTON_POINT, LOBBY_SETTINGS_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(LOBBY_SETTINGS_BUTTON_WAIT_SECONDS)
    tap_lobby_settings_button(get_context_device())


def tap_lobby_settings_button(serial: str) -> None:
    x, y = LOBBY_SETTINGS_BUTTON_POINT
    tap_point(serial, int(x), int(y), "大厅右上角设置按钮")
