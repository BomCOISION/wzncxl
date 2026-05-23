from __future__ import annotations

from config import FARM_BACK_BUTTON_POINT, FARM_BACK_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(FARM_BACK_BUTTON_WAIT_SECONDS)
    tap_farm_back_button(get_context_device())


def tap_farm_back_button(serial: str) -> None:
    x, y = FARM_BACK_BUTTON_POINT
    tap_point(serial, int(x), int(y), "农场返回按钮")
