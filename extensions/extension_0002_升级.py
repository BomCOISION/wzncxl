from __future__ import annotations

from config import (
    FARM_UPGRADE_ARROW_CLICK_POINT,
    FARM_UPGRADE_BACK_BUTTON_POINT,
    FARM_UPGRADE_BUTTON_POINT,
    FARM_UPGRADE_REPEAT_CLICK_TIMES,
    FARM_UPGRADE_RESULT_PATH,
    FARM_UPGRADE_SCAN_SCREENSHOT_PATH,
)
from common.farm_upgrade_recognizer import save_upgrade_result, scan_farm_upgrade
from common.log_utils import log_info
from common.run_context import get_context_device
from common.screenshot_utils import save_device_median_screenshot
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    serial = get_context_device()
    screen_path = save_device_median_screenshot(serial, FARM_UPGRADE_SCAN_SCREENSHOT_PATH)
    result = scan_farm_upgrade(screen_path)
    save_upgrade_result(result, FARM_UPGRADE_RESULT_PATH)
    log_upgrade_result(serial, result)
    tap_upgrade_arrow_if_needed(serial, result)


def log_upgrade_result(serial: str, result: dict) -> None:
    status = "可以升级" if result["can_upgrade"] else "不能升级"
    log_info(f"[{serial}] 农场升级判断: {status}，分数 {result['score']}/{result['threshold']}")


def tap_upgrade_arrow_if_needed(serial: str, result: dict) -> None:
    if not result["can_upgrade"]:
        return
    x, y = require_point(FARM_UPGRADE_ARROW_CLICK_POINT, "农场升级箭头")
    tap_point(serial, x, y, "农场升级箭头")
    wait_seconds(1)
    tap_upgrade_button(serial)
    repeat_tap_upgrade_button(serial)
    tap_upgrade_back_button(serial)


def tap_upgrade_button(serial: str) -> None:
    x, y = require_point(FARM_UPGRADE_BUTTON_POINT, "农场升级按钮")
    tap_point(serial, x, y, "农场升级按钮")


def repeat_tap_upgrade_button(serial: str) -> None:
    for _ in range(FARM_UPGRADE_REPEAT_CLICK_TIMES):
        wait_seconds(4)
        tap_upgrade_button(serial)
        tap_upgrade_button(serial)
        wait_seconds(4)
        tap_upgrade_button(serial)
        tap_upgrade_button(serial)


def tap_upgrade_back_button(serial: str) -> None:
    x, y = require_point(FARM_UPGRADE_BACK_BUTTON_POINT, "农场升级返回按钮")
    tap_point(serial, x, y, "农场升级返回按钮")


def require_point(point: object, label: str) -> tuple[int, int]:
    if not isinstance(point, (list, tuple)) or len(point) != 2:
        raise ValueError(f"{label}坐标必须配置为 [x, y]")
    x, y = point
    return int(x), int(y)
