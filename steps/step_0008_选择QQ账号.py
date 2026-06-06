from __future__ import annotations

from config import (
    QQ_ACCOUNT_COUNT,
    QQ_ACCOUNT_ROW_HEIGHT,
    QQ_FIRST_ACCOUNT_POINT,
)
from common.account_position_utils import calculate_account_point, calculate_index_from_bottom
from common.progress_state import get_current_account_from_bottom_index
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(1)
    tap_selected_account(get_context_device())


def tap_selected_account(serial: str) -> None:
    x, y = calculate_selected_account_point()
    tap_point(serial, x, y, build_account_label())


def calculate_selected_account_point() -> tuple[int, int]:
    index = calculate_index_from_bottom(QQ_ACCOUNT_COUNT, get_current_account_from_bottom_index())
    return calculate_account_point(QQ_FIRST_ACCOUNT_POINT, QQ_ACCOUNT_ROW_HEIGHT, index)


def build_account_label() -> str:
    return f"从下往上第 {get_current_account_from_bottom_index()} 个 QQ 账号"
