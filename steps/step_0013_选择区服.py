from __future__ import annotations

from config import (
    ADB_PATH,
    MY_SERVER_LIST_REGION,
    MY_SERVER_STATUS_TEMPLATE_PATHS,
    SERVER_SELECT_POINT_OFFSET,
)
from common.adb_client import ADBClient
from common.progress_state import get_current_server_index
from common.run_context import get_context_device
from common.server_list_counter import find_sorted_server_status_points
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(1)
    tap_selected_server(get_context_device())


def tap_selected_server(serial: str) -> None:
    x, y = calculate_selected_server_point(serial)
    tap_point(serial, x, y, f"第 {get_current_server_index()} 个区服")


def calculate_selected_server_point(serial: str) -> tuple[int, int]:
    points = find_server_points(serial)
    return offset_server_point(points[get_current_server_index() - 1])


def find_server_points(serial: str) -> list[tuple[int, int]]:
    frame = ADBClient(str(ADB_PATH), serial).median_frame(5)
    return find_sorted_server_status_points(frame, MY_SERVER_STATUS_TEMPLATE_PATHS, MY_SERVER_LIST_REGION, 0.82, 40)


def offset_server_point(point: tuple[int, int]) -> tuple[int, int]:
    offset_x, offset_y = SERVER_SELECT_POINT_OFFSET
    return int(point[0]) + int(offset_x), int(point[1]) + int(offset_y)
