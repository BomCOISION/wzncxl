from __future__ import annotations

from random import choice

from config import (
    BLESS_FRIENDS_FIRST_VISIT_BUTTON_POINT,
    BLESS_FRIENDS_FULL_COUNT_MATCH_REGION,
    BLESS_FRIENDS_FULL_COUNT_SCAN_SCREENSHOT_PATH,
    BLESS_FRIENDS_FULL_COUNT_TEMPLATE_PATH,
    BLESS_FRIENDS_HOME_BUTTON_POINT,
    BLESS_FRIENDS_LAND_INDEXES,
    BLESS_FRIENDS_RESTORE_BUTTON_POINT,
    BLESS_FRIENDS_SOCIAL_BUTTON_POINT,
    BLESS_FRIENDS_TARGET_COUNT,
    BLESS_FRIENDS_WISH_BUTTON_POINT,
    FARM_JOYSTICK_CENTER_POINT,
    OPEN_LAND_FORWARD_END_POINT,
    OPEN_LAND_LEFT_END_POINT,
    OPEN_LAND_NEXT_ROW_FORWARD_END_POINT,
    OPEN_LAND_RIGHT_END_POINT,
    OPEN_LAND_ROW_LAND_COUNT,
    OPEN_LAND_SECOND_ROW_RIGHT_COUNT,
    OPEN_LAND_THIRD_ROW_LEFT_COUNT,
)
from common.config_point_utils import require_point
from common.log_utils import log_info
from common.run_context import get_context_device
from common.screenshot_utils import save_device_median_screenshot
from common.single_template_finder import find_template_center
from common.template_matcher import read_image_file
from common.touch_utils import hold_drag_point, tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    serial = get_context_device()
    blessed_count = run_bless_rounds(serial, get_configured_land_indexes())
    log_stop_if_unfinished(serial, blessed_count)


def run_bless_rounds(serial: str, candidate_land_indexes: list[int]) -> int:
    blessed_count = 0
    while blessed_count < BLESS_FRIENDS_TARGET_COUNT and candidate_land_indexes:
        land_index = choice(candidate_land_indexes)
        if bless_configured_land(serial, land_index):
            blessed_count = log_bless_success(serial, blessed_count)
        else:
            candidate_land_indexes.remove(land_index)
    return blessed_count


def get_configured_land_indexes() -> list[int]:
    land_indexes = list(dict.fromkeys(BLESS_FRIENDS_LAND_INDEXES))
    validate_land_indexes(land_indexes)
    return land_indexes


def validate_land_indexes(land_indexes: list[int]) -> None:
    if not land_indexes:
        raise ValueError("祝福好友土地列表不能为空")
    invalid = [land_index for land_index in land_indexes if not is_supported_land_index(land_index)]
    if invalid:
        raise ValueError(f"祝福好友土地编号超出范围: {invalid}")


def is_supported_land_index(land_index: int) -> bool:
    return 1 <= land_index <= get_total_land_count()


def log_bless_success(serial: str, blessed_count: int) -> int:
    blessed_count += 1
    log_info(f"[{serial}] 祝福好友完成 {blessed_count}/{BLESS_FRIENDS_TARGET_COUNT}")
    return blessed_count


def log_stop_if_unfinished(serial: str, blessed_count: int) -> None:
    if blessed_count < BLESS_FRIENDS_TARGET_COUNT:
        log_info(f"[{serial}] 祝福好友候选土地都已满，停止祝福")


def bless_configured_land(serial: str, land_index: int) -> bool:
    log_info(f"[{serial}] 随机选择祝福好友第 {land_index} 块土地")
    enter_first_friend_farm(serial)
    prepare_friend_farm(serial)
    move_to_land(serial, land_index)
    return bless_current_land_and_return_home(serial, land_index)


def enter_first_friend_farm(serial: str) -> None:
    tap_restore_button(serial)
    wait_seconds(0.5)
    tap_social_button(serial)
    wait_seconds(0.8)
    tap_first_visit_button(serial)
    wait_seconds(10)


def prepare_friend_farm(serial: str) -> None:
    tap_restore_button(serial)
    wait_seconds(1)


def bless_current_land_and_return_home(serial: str, land_index: int) -> bool:
    if is_current_land_fully_blessed(serial):
        log_info(f"[{serial}] 第 {land_index} 块土地祝福次数已满，跳过")
        tap_home_button(serial)
        wait_seconds(10)
        return False
    tap_wish_button(serial)
    wait_seconds(0.544)
    tap_home_button(serial)
    wait_seconds(10)
    return True


def is_current_land_fully_blessed(serial: str) -> bool:
    for _ in range(2):
        if not detect_full_count_once(serial):
            return False
        wait_seconds(0.1)
    return True


def detect_full_count_once(serial: str) -> bool:
    screen_path = save_device_median_screenshot(serial, BLESS_FRIENDS_FULL_COUNT_SCAN_SCREENSHOT_PATH)
    image = read_image_file(screen_path)
    point = find_template_center(image, BLESS_FRIENDS_FULL_COUNT_TEMPLATE_PATH, 0.9, BLESS_FRIENDS_FULL_COUNT_MATCH_REGION)
    return point is not None


def tap_restore_button(serial: str) -> None:
    x, y = require_point(BLESS_FRIENDS_RESTORE_BUTTON_POINT, "祝福好友还原按钮")
    tap_point(serial, x, y, "祝福好友还原按钮")


def tap_social_button(serial: str) -> None:
    x, y = require_point(BLESS_FRIENDS_SOCIAL_BUTTON_POINT, "祝福好友社交图标")
    tap_point(serial, x, y, "祝福好友社交图标")


def tap_first_visit_button(serial: str) -> None:
    x, y = require_point(BLESS_FRIENDS_FIRST_VISIT_BUTTON_POINT, "第一个好友拜访按钮")
    tap_point(serial, x, y, "第一个好友拜访按钮")


def tap_wish_button(serial: str) -> None:
    x, y = require_point(BLESS_FRIENDS_WISH_BUTTON_POINT, "祝福按钮")
    tap_point(serial, x, y, "祝福按钮")


def tap_home_button(serial: str) -> None:
    x, y = require_point(BLESS_FRIENDS_HOME_BUTTON_POINT, "回家按钮")
    tap_point(serial, x, y, "回家按钮")


def move_to_land(serial: str, target_land_index: int) -> None:
    side, local_land_index = calculate_land_position(target_land_index)
    move_to_first_land(serial, side)
    for land_index in range(1, local_land_index):
        move_to_next_land(serial, side, land_index)


def calculate_land_position(land_index: int) -> tuple[str, int]:
    side_land_count = get_side_land_count()
    if land_index <= side_land_count:
        return "left", land_index
    return "right", land_index - side_land_count


def move_to_first_land(serial: str, side: str) -> None:
    run_forward(serial)
    if side == "left":
        run_left(serial)
    else:
        run_right(serial)


def move_to_next_land(serial: str, side: str, land_index: int) -> None:
    if land_index < OPEN_LAND_ROW_LAND_COUNT:
        move_first_row(serial, side)
    elif land_index == OPEN_LAND_ROW_LAND_COUNT:
        run_short_forward(serial)
    elif land_index < get_second_row_last_index():
        move_second_row(serial, side)
    elif land_index == get_second_row_last_index():
        run_short_forward(serial)
    else:
        move_third_row(serial, side)


def move_first_row(serial: str, side: str) -> None:
    if side == "left":
        run_left(serial)
    else:
        run_right(serial)


def move_second_row(serial: str, side: str) -> None:
    if side == "left":
        run_right(serial)
    else:
        run_left(serial)


def move_third_row(serial: str, side: str) -> None:
    move_first_row(serial, side)


def get_second_row_last_index() -> int:
    return OPEN_LAND_ROW_LAND_COUNT + 1 + OPEN_LAND_SECOND_ROW_RIGHT_COUNT


def get_side_land_count() -> int:
    return (
        OPEN_LAND_ROW_LAND_COUNT
        + 1
        + OPEN_LAND_SECOND_ROW_RIGHT_COUNT
        + 1
        + OPEN_LAND_THIRD_ROW_LEFT_COUNT
    )


def get_total_land_count() -> int:
    return get_side_land_count() * 2


def run_forward(serial: str) -> None:
    start = require_point(FARM_JOYSTICK_CENTER_POINT, "农场方向键中心")
    end = require_point(OPEN_LAND_FORWARD_END_POINT, "祝福好友正前方终点")
    hold_drag_point(serial, start, end, 100, 1300, "祝福好友正前方奔跑")


def run_left(serial: str) -> None:
    start = require_point(FARM_JOYSTICK_CENTER_POINT, "农场方向键中心")
    end = require_point(OPEN_LAND_LEFT_END_POINT, "祝福好友正左方终点")
    hold_drag_point(serial, start, end, 100, 200, "祝福好友正左方移动")


def run_short_forward(serial: str) -> None:
    start = require_point(FARM_JOYSTICK_CENTER_POINT, "农场方向键中心")
    end = require_point(OPEN_LAND_NEXT_ROW_FORWARD_END_POINT, "祝福好友下一行正前方终点")
    hold_drag_point(serial, start, end, 100, 200, "祝福好友下一行正前方移动")


def run_right(serial: str) -> None:
    start = require_point(FARM_JOYSTICK_CENTER_POINT, "农场方向键中心")
    end = require_point(OPEN_LAND_RIGHT_END_POINT, "祝福好友正右方终点")
    hold_drag_point(serial, start, end, 100, 200, "祝福好友正右方移动")
