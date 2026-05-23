from __future__ import annotations

from config import ONE_CLICK_FARM_BUTTON_POINT, ONE_CLICK_FARM_BUTTON_WAIT_SECONDS
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(ONE_CLICK_FARM_BUTTON_WAIT_SECONDS)
    tap_one_click_farm_button(get_context_device())


def tap_one_click_farm_button(serial: str) -> None:
    x, y = ONE_CLICK_FARM_BUTTON_POINT
    tap_point(serial, int(x), int(y), "一键务农按钮")
