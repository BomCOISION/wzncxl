from __future__ import annotations

from collections.abc import Callable

from config import (
    FARM_JOYSTICK_CENTER_POINT,
    OPEN_LAND_CANCEL_BUTTON_POINT,
    OPEN_LAND_CULTIVATE_BUTTON_POINT,
    OPEN_LAND_CONFIRM_BUTTON_POINT,
    OPEN_LAND_FORWARD_END_POINT,
    OPEN_LAND_LEFT_END_POINT,
    OPEN_LAND_LEVEL_NOT_ENOUGH_CLOSE_POINT,
    OPEN_LAND_NEXT_ROW_FORWARD_END_POINT,
    OPEN_LAND_RESTORE_BUTTON_POINT,
    OPEN_LAND_RIGHT_END_POINT,
    OPEN_LAND_ROW_LAND_COUNT,
    OPEN_LAND_SECOND_ROW_RIGHT_COUNT,
    OPEN_LAND_THIRD_ROW_LEFT_COUNT,
)
from common.config_point_utils import require_point
from common.run_context import get_context_device
from common.touch_utils import hold_drag_point, tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    serial = get_context_device()
    # restore_position(serial)
    # run_forward(serial)
    # cultivate_left_plot(serial)
    restore_position(serial)
    run_forward(serial)
    cultivate_right_plot(serial)
    restore_position(serial)


def restore_position(serial: str) -> None:
    wait_seconds(1)
    tap_open_land_restore_button(serial)


def tap_open_land_restore_button(serial: str) -> None:
    x, y = require_point(OPEN_LAND_RESTORE_BUTTON_POINT, "开土地还原位置按钮")
    tap_point(serial, x, y, "开土地还原位置按钮")


def run_forward(serial: str) -> None:
    wait_seconds(1)
    start = require_point(FARM_JOYSTICK_CENTER_POINT, "农场方向键中心")
    end = require_point(OPEN_LAND_FORWARD_END_POINT, "开土地正前方终点")
    hold_drag_point(serial, start, end, 100, 1250, "开土地正前方奔跑")


def run_left(serial: str) -> None:
    end = require_point(OPEN_LAND_LEFT_END_POINT, "开土地正左方终点")
    drag_joystick(serial, end, 100, 200, "开土地正左方移动")


def run_short_forward(serial: str) -> None:
    end = require_point(OPEN_LAND_NEXT_ROW_FORWARD_END_POINT, "开土地下一行正前方终点")
    drag_joystick(serial, end, 100, 200, "开土地下一行正前方移动")


def run_right(serial: str) -> None:
    end = require_point(OPEN_LAND_RIGHT_END_POINT, "开土地正右方终点")
    drag_joystick(serial, end, 100, 200, "开土地正右方移动")


def drag_joystick(serial: str, end: tuple[int, int], move_ms: int, hold_ms: int, label: str) -> None:
    start = require_point(FARM_JOYSTICK_CENTER_POINT, "农场方向键中心")
    hold_drag_point(serial, start, end, move_ms, hold_ms, label)


def cultivate_left_plot(serial: str) -> None:
    cultivate_left_plot_first_row(serial)
    cultivate_left_plot_second_row(serial)
    cultivate_left_plot_third_row(serial)


def cultivate_right_plot(serial: str) -> None:
    cultivate_right_plot_first_row(serial)
    cultivate_right_plot_second_row(serial)
    cultivate_right_plot_third_row(serial)


def cultivate_left_plot_first_row(serial: str) -> None:
    cultivate_lands_with_move(serial, run_left, OPEN_LAND_ROW_LAND_COUNT)


def cultivate_left_plot_second_row(serial: str) -> None:
    run_short_forward(serial)
    cultivate_current_land(serial)
    cultivate_lands_with_move(serial, run_right, OPEN_LAND_SECOND_ROW_RIGHT_COUNT)


def cultivate_left_plot_third_row(serial: str) -> None:
    run_short_forward(serial)
    cultivate_current_land(serial)
    cultivate_lands_with_move(serial, run_left, OPEN_LAND_THIRD_ROW_LEFT_COUNT)


def cultivate_right_plot_first_row(serial: str) -> None:
    cultivate_lands_with_move(serial, run_right, OPEN_LAND_ROW_LAND_COUNT)


def cultivate_right_plot_second_row(serial: str) -> None:
    run_short_forward(serial)
    cultivate_current_land(serial)
    cultivate_lands_with_move(serial, run_left, OPEN_LAND_SECOND_ROW_RIGHT_COUNT)


def cultivate_right_plot_third_row(serial: str) -> None:
    run_short_forward(serial)
    cultivate_current_land(serial)
    cultivate_lands_with_move(serial, run_right, OPEN_LAND_THIRD_ROW_LEFT_COUNT)


def cultivate_lands_with_move(serial: str, move_func: Callable[[str], None], count: int) -> None:
    for _ in range(count):
        move_func(serial)
        cultivate_current_land(serial)


def cultivate_current_land(serial: str) -> None:
    tap_cultivate_button(serial)
    wait_seconds(0.5)
    tap_confirm_button(serial)
    wait_seconds(0.5)
    tap_cancel_button(serial)
    wait_seconds(3)
    close_level_not_enough_popup(serial)


def tap_cultivate_button(serial: str) -> None:
    x, y = require_point(OPEN_LAND_CULTIVATE_BUTTON_POINT, "开垦按钮")
    tap_point(serial, x, y, "开垦按钮")


def tap_confirm_button(serial: str) -> None:
    x, y = require_point(OPEN_LAND_CONFIRM_BUTTON_POINT, "开垦确定按钮")
    tap_point(serial, x, y, "开垦确定按钮")


def tap_cancel_button(serial: str) -> None:
    x, y = require_point(OPEN_LAND_CANCEL_BUTTON_POINT, "开垦取消按钮")
    tap_point(serial, x, y, "开垦取消按钮")


def close_level_not_enough_popup(serial: str) -> None:
    wait_seconds(1)
    x, y = require_point(OPEN_LAND_LEVEL_NOT_ENOUGH_CLOSE_POINT, "开土地等级不够弹窗关闭按钮")
    tap_point(serial, x, y, "开土地等级不够弹窗关闭按钮")
