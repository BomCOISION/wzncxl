from __future__ import annotations

from config import (
    ADB_PATH,
    MY_SERVER_LIST_REGION,
    MY_SERVER_STATUS_TEMPLATE_PATHS,
    SCREENSHOT_MEDIAN_FRAME_COUNT,
    SERVER_STATUS_DEDUP_DISTANCE,
    SERVER_STATUS_MATCH_THRESHOLD,
)
from common.adb_client import ADBClient
from common.log_utils import log_info
from common.progress_state import save_current_server_count
from common.run_context import get_context_device
from common.server_list_counter import count_server_status_icons


def run() -> None:
    count_my_servers(get_context_device())


def count_my_servers(serial: str) -> None:
    count = calculate_server_count(serial)
    save_current_server_count(count)
    log_info(f"[{serial}] 我的服务器列表识别到 {count} 个区")


def calculate_server_count(serial: str) -> int:
    frame = ADBClient(str(ADB_PATH), serial).median_frame(SCREENSHOT_MEDIAN_FRAME_COUNT)
    return count_server_status_icons(frame, MY_SERVER_STATUS_TEMPLATE_PATHS, MY_SERVER_LIST_REGION, SERVER_STATUS_MATCH_THRESHOLD, SERVER_STATUS_DEDUP_DISTANCE)
