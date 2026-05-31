from __future__ import annotations

from config import START_GAME_BUTTON_POINT, START_GAME_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(START_GAME_BUTTON_WAIT_SECONDS)
    tap_start_game_button(get_context_device())
    wait_seconds(4)
    tap_start_game_button(get_context_device())


def tap_start_game_button(serial: str) -> None:
    x, y = START_GAME_BUTTON_POINT
    tap_point(serial, int(x), int(y), "开始游戏按钮")
