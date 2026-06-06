from __future__ import annotations

from config import (
    PIN_FRIEND_AVATAR_MATCH_REGION,
    PIN_FRIEND_AVATAR_SCAN_SCREENSHOT_PATH,
    PIN_FRIEND_AVATAR_TEMPLATE_PATH,
    PIN_FRIEND_FIRST_AVATAR_CENTER_Y,
    PIN_FRIEND_MORE_BUTTON_X,
    PIN_FRIEND_MORE_BUTTON_Y_OFFSET,
    PIN_FRIEND_RESTORE_BUTTON_POINT,
    PIN_FRIEND_ROW_HEIGHT,
    PIN_FRIEND_SOCIAL_BUTTON_POINT,
)
from common.config_point_utils import require_point
from common.log_utils import log_info
from common.run_context import get_context_device
from common.screenshot_utils import save_device_median_screenshot
from common.single_template_finder import find_template_center
from common.template_matcher import read_image_file
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    serial = get_context_device()
    open_friend_list(serial)
    avatar_center = find_friend_avatar(serial)
    tap_more_button(serial, avatar_center)


def open_friend_list(serial: str) -> None:
    tap_restore_button(serial)
    wait_seconds(0.5)
    tap_social_button(serial)
    wait_seconds(0.8)


def find_friend_avatar(serial: str) -> tuple[int, int]:
    screen_path = save_device_median_screenshot(serial, PIN_FRIEND_AVATAR_SCAN_SCREENSHOT_PATH)
    image = read_image_file(screen_path)
    point = find_template_center(image, PIN_FRIEND_AVATAR_TEMPLATE_PATH, 0.9, PIN_FRIEND_AVATAR_MATCH_REGION)
    if point is None:
        raise RuntimeError(f"[{serial}] 未找到置顶好友头像")
    log_info(f"[{serial}] 找到置顶好友头像: {point}")
    return point


def tap_more_button(serial: str, avatar_center: tuple[int, int]) -> None:
    row_index = calculate_friend_row_index(avatar_center)
    x, y = calculate_more_button_point(avatar_center)
    log_info(f"[{serial}] 置顶好友在第 {row_index} 个可见位置，更多按钮: ({x}, {y})")
    tap_point(serial, x, y, "置顶好友更多按钮")


def calculate_friend_row_index(avatar_center: tuple[int, int]) -> int:
    row_offset = avatar_center[1] - PIN_FRIEND_FIRST_AVATAR_CENTER_Y
    return max(1, round(row_offset / PIN_FRIEND_ROW_HEIGHT) + 1)


def calculate_more_button_point(avatar_center: tuple[int, int]) -> tuple[int, int]:
    x = int(PIN_FRIEND_MORE_BUTTON_X)
    y = int(avatar_center[1] + PIN_FRIEND_MORE_BUTTON_Y_OFFSET)
    return x, y


def tap_restore_button(serial: str) -> None:
    x, y = require_point(PIN_FRIEND_RESTORE_BUTTON_POINT, "置顶好友还原按钮")
    tap_point(serial, x, y, "置顶好友还原按钮")


def tap_social_button(serial: str) -> None:
    x, y = require_point(PIN_FRIEND_SOCIAL_BUTTON_POINT, "置顶好友社交图标")
    tap_point(serial, x, y, "置顶好友社交图标")
