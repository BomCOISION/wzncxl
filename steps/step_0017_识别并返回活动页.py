from __future__ import annotations

from config import (
    ACTIVITY_BACK_BUTTON_MATCH_THRESHOLD,
    ACTIVITY_BACK_BUTTON_TEMPLATE_PATH,
    ACTIVITY_BACK_BUTTON_WAIT_SECONDS,
    ADB_PATH,
    SCREENSHOT_MEDIAN_FRAME_COUNT,
)
from common.adb_client import ADBClient
from common.log_utils import log_info
from common.run_context import get_context_device
from common.single_template_finder import find_template_center
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(ACTIVITY_BACK_BUTTON_WAIT_SECONDS)
    back_activity_if_exists(get_context_device())


def back_activity_if_exists(serial: str) -> None:
    point = find_activity_back_point(serial)
    if point is None:
        log_info(f"[{serial}] 未识别到活动页返回按钮，跳过")
        return
    tap_point(serial, point[0], point[1], "活动页返回按钮")


def back_activity(serial: str) -> bool:
    point = find_activity_back_point(serial)
    if point is None:
        return False
    tap_point(serial, point[0], point[1], "活动页返回按钮")
    return True


def find_activity_back_point(serial: str) -> tuple[int, int] | None:
    frame = ADBClient(str(ADB_PATH), serial).median_frame(SCREENSHOT_MEDIAN_FRAME_COUNT)
    return find_template_center(frame, ACTIVITY_BACK_BUTTON_TEMPLATE_PATH, ACTIVITY_BACK_BUTTON_MATCH_THRESHOLD)
