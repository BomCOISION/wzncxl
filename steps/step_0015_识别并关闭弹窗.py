from __future__ import annotations

from config import (
    ADB_PATH,
    POPUP_CLOSE_X_MATCH_REGION,
    POPUP_CLOSE_X_TEMPLATE_PATH,
)
from common.adb_client import ADBClient
from common.log_utils import log_info
from common.run_context import get_context_device
from common.single_template_finder import find_template_center
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(1)
    close_popup_if_exists(get_context_device())


def close_popup_if_exists(serial: str) -> None:
    point = find_popup_close_point(serial)
    if point is None:
        log_info(f"[{serial}] 未识别到弹窗关闭按钮，跳过")
        return
    tap_point(serial, point[0], point[1], "弹窗关闭按钮")


def close_popup(serial: str) -> bool:
    point = find_popup_close_point(serial)
    if point is None:
        return False
    tap_point(serial, point[0], point[1], "弹窗关闭按钮")
    return True


def find_popup_close_point(serial: str) -> tuple[int, int] | None:
    frame = ADBClient(str(ADB_PATH), serial).median_frame(5)
    return find_template_center(
        frame,
        POPUP_CLOSE_X_TEMPLATE_PATH,
        0.82,
        POPUP_CLOSE_X_MATCH_REGION,
    )
