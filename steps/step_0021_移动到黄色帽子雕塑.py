from __future__ import annotations

from config import (
    FARM_JOYSTICK_CENTER_POINT,
    FARM_RUN_LEFT_UP_END_POINT,
)
from common.run_context import get_context_device
from common.touch_utils import swipe_point
from common.wait_utils import wait_seconds


def run() -> None:
    move_to_hat_statue(get_context_device())


def move_to_hat_statue(serial: str) -> None:
    wait_seconds(1)
    start = to_int_point(FARM_JOYSTICK_CENTER_POINT)
    end = to_int_point(FARM_RUN_LEFT_UP_END_POINT)
    swipe_point(serial, start, end, 1900, "到黄色帽子雕塑")


def to_int_point(point: tuple) -> tuple[int, int]:
    x, y = point
    return int(x), int(y)
