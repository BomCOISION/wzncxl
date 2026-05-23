from __future__ import annotations

from config import ADB_PATH
from common.adb_client import ADBClient
from common.log_utils import log_info


def tap_point(serial: str, x: int, y: int, label: str) -> None:
    log_info(f"[{serial}] 点击{label}: ({x}, {y})")
    ADBClient(str(ADB_PATH), serial).tap(x, y)


def swipe_point(serial: str, start: tuple[int, int], end: tuple[int, int], duration_ms: int, label: str) -> None:
    log_info(f"[{serial}] 滑动{label}: {start} -> {end}, {duration_ms}ms")
    ADBClient(str(ADB_PATH), serial).swipe(start[0], start[1], end[0], end[1], duration_ms)
