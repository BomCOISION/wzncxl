from __future__ import annotations

from config import (
    ADB_PATH,
    MY_SERVER_LIST_REGION,
    MY_SERVER_STATUS_TEMPLATE_PATHS,
)
from common.adb_client import ADBClient
from common.log_utils import log_info
from common.progress_state import get_current_server_count, save_current_server_count
from common.run_context import get_context_device
from common.server_list_counter import count_server_status_icons


def run() -> None:
    count_my_servers(get_context_device())


def count_my_servers(serial: str) -> None:
    if use_cached_server_count(serial):
        return
    count = calculate_server_count(serial)
    save_current_server_count(count)
    log_info(f"[{serial}] 我的服务器列表识别到 {count} 个区")


def use_cached_server_count(serial: str) -> bool:
    count = get_current_server_count()
    if count <= 0:
        return False
    log_info(f"[{serial}] 复用当前账号已识别区服数量 {count} 个")
    return True


def calculate_server_count(serial: str) -> int:
    frame = ADBClient(str(ADB_PATH), serial).median_frame(5)
    return count_server_status_icons(frame, MY_SERVER_STATUS_TEMPLATE_PATHS, MY_SERVER_LIST_REGION, 0.82, 40)
