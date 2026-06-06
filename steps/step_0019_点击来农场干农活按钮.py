from __future__ import annotations

from time import monotonic

from config import FARM_WORK_BUTTON_POINT
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    tap_farm_work_button_repeatedly(get_context_device())


def tap_farm_work_button_repeatedly(serial: str) -> None:
    end_time = monotonic() + 5
    while monotonic() < end_time:
        tap_farm_work_button(serial)
        wait_seconds(1)


def tap_farm_work_button(serial: str) -> None:
    x, y = FARM_WORK_BUTTON_POINT
    tap_point(serial, int(x), int(y), "来农场干农活按钮")
