from __future__ import annotations

from config import ADB_PATH
from common.adb_client import ADBClient
from common.log_utils import log_info


def tap_point(serial: str, x: int, y: int, label: str) -> None:
    log_info(f"[{serial}] 点击{label}: ({x}, {y})")
    ADBClient(str(ADB_PATH), serial).tap(x, y)
