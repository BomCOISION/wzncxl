from __future__ import annotations

from config import CURRENT_INTERFACE_CLICK_POINT
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(1)
    tap_current_interface_position(get_context_device())


def tap_current_interface_position(serial: str) -> None:
    x, y = CURRENT_INTERFACE_CLICK_POINT
    tap_point(serial, int(x), int(y), "当前界面指定位置")
