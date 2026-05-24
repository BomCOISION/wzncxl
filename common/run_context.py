from __future__ import annotations

from random import choice
from subprocess import CompletedProcess

from config import ADB_PATH, TARGET_DEVICES
from common.adb_client import run_adb_process
from common.log_utils import log_info

_CONTEXT_DEVICES: list[str] | None = None


def get_context_device() -> str:
    return get_context_devices()[0]


def get_context_devices() -> list[str]:
    """获取当前执行设备列表"""
    global _CONTEXT_DEVICES
    if _CONTEXT_DEVICES is None:
        _CONTEXT_DEVICES = resolve_context_devices()
    return list(_CONTEXT_DEVICES)


def resolve_context_devices() -> list[str]:
    online_devices = list_online_devices()
    configured_devices = get_online_configured_devices(online_devices)
    if configured_devices:
        return configured_devices
    return [choose_random_online_device(online_devices)]


def get_online_configured_devices(online_devices: list[str]) -> list[str]:
    online_set = set(online_devices)
    return [serial for serial in TARGET_DEVICES if serial in online_set]


def choose_random_online_device(online_devices: list[str]) -> str:
    if not online_devices:
        raise ValueError("没有找到在线 ADB 设备")
    serial = choice(online_devices)
    log_info(f"[{serial}] 配置设备不可用，随机选择在线设备")
    return serial


def list_online_devices() -> list[str]:
    result = run_adb_process([str(ADB_PATH), "devices"], text=True)
    check_adb_devices_result(result)
    rows = result.stdout.splitlines()[1:]
    return [row.split()[0] for row in rows if is_online_device_row(row)]


def check_adb_devices_result(result: CompletedProcess[str]) -> None:
    if result.returncode:
        error = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(error or "adb devices 执行失败")


def is_online_device_row(row: str) -> bool:
    parts = row.split()
    return len(parts) >= 2 and parts[1] == "device"
