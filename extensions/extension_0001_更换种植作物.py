from __future__ import annotations

from config import (
    CHANGE_CROP_AFTER_FIRST_CROP_WAIT_SECONDS,
    CHANGE_CROP_AFTER_TARGET_CROP_WAIT_SECONDS,
    CHANGE_CROP_DELETE_WAIT_SECONDS,
    CHANGE_CROP_DELETE_X_BUTTON_POINT,
    CHANGE_CROP_FIRST_CROP_POINT,
    CHANGE_CROP_PLANT_BUTTON_POINT,
    CHANGE_CROP_PLANT_WAIT_SECONDS,
    CHANGE_CROP_SELECT_BUTTON_POINT,
    CROP_LIST_RESULT_PATH,
    CROP_LIST_SCAN_SCREENSHOT_PATH,
)
from common.crop_list_recognizer import save_crop_scan_result, scan_crop_list
from common.run_context import get_context_device
from common.screenshot_utils import save_device_screenshot
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    serial = get_context_device()
    wait_seconds(CHANGE_CROP_DELETE_WAIT_SECONDS)
    tap_delete_current_crop(serial)
    wait_seconds(CHANGE_CROP_PLANT_WAIT_SECONDS)
    tap_plant_button(serial)
    wait_seconds(1)
    tap_first_crop(serial)
    wait_seconds(CHANGE_CROP_AFTER_FIRST_CROP_WAIT_SECONDS)
    tap_target_crop(serial)
    wait_seconds(CHANGE_CROP_AFTER_TARGET_CROP_WAIT_SECONDS)
    tap_select_button(serial)


def tap_delete_current_crop(serial: str) -> None:
    x, y = require_point(CHANGE_CROP_DELETE_X_BUTTON_POINT, "种植按钮X键")
    tap_point(serial, x, y, "种植按钮X键")


def tap_plant_button(serial: str) -> None:
    x, y = require_point(CHANGE_CROP_PLANT_BUTTON_POINT, "种植按钮")
    tap_point(serial, x, y, "种植按钮")


def tap_first_crop(serial: str) -> None:
    x, y = require_point(CHANGE_CROP_FIRST_CROP_POINT, "第一个农作物")
    tap_point(serial, x, y, "第一个农作物")


def tap_target_crop(serial: str) -> None:
    point = get_priority_crop_icon_by_flag(serial, 1)
    x, y = require_found_point(point, "优先级1农作物")
    tap_point(serial, x, y, "优先级1农作物")


def get_priority_crop_icon_by_flag(serial: str, flag: int) -> list[int] | None:
    screen_path = save_device_screenshot(serial, CROP_LIST_SCAN_SCREENSHOT_PATH)
    result = scan_crop_list(screen_path)
    save_crop_scan_result(result, CROP_LIST_RESULT_PATH)
    return get_priority_icon_point(result, flag)


def get_priority_icon_point(result: dict, flag: int) -> list[int] | None:
    target = result.get("priority_crop_icons", {}).get(str(flag))
    return None if target is None else target["point"]


def tap_select_button(serial: str) -> None:
    x, y = require_point(CHANGE_CROP_SELECT_BUTTON_POINT, "选择按钮")
    tap_point(serial, x, y, "选择按钮")


def require_found_point(point: object, label: str) -> tuple[int, int]:
    if point is None:
        raise ValueError(f"未找到{label}")
    return require_point(point, label)


def require_point(point: object, label: str) -> tuple[int, int]:
    if not isinstance(point, (list, tuple)) or len(point) != 2:
        raise ValueError(f"{label}坐标必须配置为 [x, y]")
    x, y = point
    if int(x) == 0 and int(y) == 0:
        raise ValueError(f"{label}坐标未配置")
    return int(x), int(y)
