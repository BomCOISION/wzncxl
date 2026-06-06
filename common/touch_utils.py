from __future__ import annotations

from time import sleep

from config import ADB_PATH
from common.adb_client import ADBClient
from common.log_utils import log_info


def tap_point(serial: str, x: int, y: int, label: str) -> None:
    log_info(f"[{serial}] 点击{label}: ({x}, {y})")
    ADBClient(str(ADB_PATH), serial).tap(x, y)


def swipe_point(serial: str, start: tuple[int, int], end: tuple[int, int], duration_ms: int, label: str) -> None:
    log_info(f"[{serial}] 滑动{label}: {start} -> {end}, {duration_ms}ms")
    ADBClient(str(ADB_PATH), serial).swipe(start[0], start[1], end[0], end[1], duration_ms)


def hold_drag_point(serial: str, start: tuple[int, int], end: tuple[int, int], move_ms: int, hold_ms: int, label: str) -> None:
    log_info(f"[{serial}] 按住拖动{label}: {start} -> {end}, 移动{move_ms}ms, 保持{hold_ms}ms")
    client = ADBClient(str(ADB_PATH), serial)
    client.motion_event("DOWN", start[0], start[1])
    try:
        move_pointer_over_duration(client, start, end, move_ms)
        sleep(hold_ms / 1000)
    finally:
        client.motion_event("UP", end[0], end[1])


def move_pointer_over_duration(client: ADBClient, start: tuple[int, int], end: tuple[int, int], duration_ms: int) -> None:
    steps = max(1, duration_ms // 20)
    interval_seconds = duration_ms / steps / 1000
    for step in range(1, steps + 1):
        x, y = interpolate_point(start, end, step / steps)
        client.motion_event("MOVE", x, y)
        sleep(interval_seconds)


def interpolate_point(start: tuple[int, int], end: tuple[int, int], ratio: float) -> tuple[int, int]:
    x = start[0] + (end[0] - start[0]) * ratio
    y = start[1] + (end[1] - start[1]) * ratio
    return round(x), round(y)
