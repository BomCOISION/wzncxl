from __future__ import annotations

from config import (
    SELL_WAREHOUSE_AFTER_BATCH_SELL_WAIT_SECONDS,
    SELL_WAREHOUSE_AFTER_OPEN_WAIT_SECONDS,
    SELL_WAREHOUSE_AFTER_SELECT_ALL_WAIT_SECONDS,
    SELL_WAREHOUSE_AFTER_SECOND_SELL_WAIT_SECONDS,
    SELL_WAREHOUSE_AFTER_SELL_WAIT_SECONDS,
    SELL_WAREHOUSE_BATCH_SELL_BUTTON_POINT,
    SELL_WAREHOUSE_BUTTON_POINT,
    SELL_WAREHOUSE_CLOSE_BUTTON_POINT,
    SELL_WAREHOUSE_CONFIRM_SELL_BUTTON_POINT,
    SELL_WAREHOUSE_SELECT_ALL_POINT,
)
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    serial = get_context_device()
    tap_warehouse_button(serial)
    wait_seconds(SELL_WAREHOUSE_AFTER_OPEN_WAIT_SECONDS)
    tap_batch_sell_button(serial)
    wait_seconds(SELL_WAREHOUSE_AFTER_BATCH_SELL_WAIT_SECONDS)
    tap_select_all(serial)
    wait_seconds(SELL_WAREHOUSE_AFTER_SELECT_ALL_WAIT_SECONDS)
    tap_confirm_sell_twice(serial)
    wait_seconds(SELL_WAREHOUSE_AFTER_SECOND_SELL_WAIT_SECONDS)
    tap_close_button(serial)


def tap_warehouse_button(serial: str) -> None:
    tap_configured_point(serial, SELL_WAREHOUSE_BUTTON_POINT, "仓库按钮")


def tap_batch_sell_button(serial: str) -> None:
    tap_configured_point(serial, SELL_WAREHOUSE_BATCH_SELL_BUTTON_POINT, "批量出售按钮")


def tap_select_all(serial: str) -> None:
    tap_configured_point(serial, SELL_WAREHOUSE_SELECT_ALL_POINT, "选择全部选项框")


def tap_confirm_sell_twice(serial: str) -> None:
    tap_confirm_sell_button(serial)
    wait_seconds(SELL_WAREHOUSE_AFTER_SELL_WAIT_SECONDS)
    tap_confirm_sell_button(serial)


def tap_confirm_sell_button(serial: str) -> None:
    tap_configured_point(serial, SELL_WAREHOUSE_CONFIRM_SELL_BUTTON_POINT, "出售按钮")


def tap_close_button(serial: str) -> None:
    tap_configured_point(serial, SELL_WAREHOUSE_CLOSE_BUTTON_POINT, "仓库关闭按钮")


def tap_configured_point(serial: str, point: object, label: str) -> None:
    x, y = require_point(point, label)
    tap_point(serial, x, y, label)


def require_point(point: object, label: str) -> tuple[int, int]:
    if not isinstance(point, (list, tuple)) or len(point) != 2:
        raise ValueError(f"{label}坐标必须配置为 [x, y]")
    x, y = point
    return int(x), int(y)
