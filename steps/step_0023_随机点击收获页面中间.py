from __future__ import annotations

from config import HARVEST_CONTINUE_TEXT_POINT
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(7)
    tap_harvest_continue_area(get_context_device())


def tap_harvest_continue_area(serial: str) -> None:
    x, y = HARVEST_CONTINUE_TEXT_POINT
    tap_point(serial, int(x), int(y), "收获页面点击继续文本")
