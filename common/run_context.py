from __future__ import annotations

import atexit
from subprocess import CompletedProcess

from config import ADB_PATH, TARGET_DEVICE_LIST_CONFIGURED, TARGET_DEVICES
from common.adb_client import run_adb_process
from common.device_lock import acquire_device_lock, release_device_lock
from common.log_utils import log_info

_CONTEXT_DEVICES: list[str] | None = None
_CONTEXT_RELEASE_REGISTERED = False


def get_context_device() -> str:
    return get_context_devices()[0]


def get_context_devices() -> list[str]:
    """获取当前执行设备列表"""
    global _CONTEXT_DEVICES
    if _CONTEXT_DEVICES is None:
        _CONTEXT_DEVICES = resolve_context_devices()
        register_context_release()
    return list(_CONTEXT_DEVICES)


def resolve_context_devices() -> list[str]:
    online_devices = list_online_devices()
    serial = acquire_device_lock(get_candidate_devices(online_devices))
    log_info(f"[{serial}] 已占用设备")
    return [serial]


def get_candidate_devices(online_devices: list[str]) -> list[str]:
    configured_devices = get_online_configured_devices(online_devices)
    if TARGET_DEVICE_LIST_CONFIGURED:
        return configured_devices
    return append_online_fallback(configured_devices, online_devices)


def append_online_fallback(configured_devices: list[str], online_devices: list[str]) -> list[str]:
    if configured_devices:
        return configured_devices + [serial for serial in online_devices if serial not in configured_devices]
    return online_devices


def get_online_configured_devices(online_devices: list[str]) -> list[str]:
    online_set = set(online_devices)
    return [serial for serial in TARGET_DEVICES if serial in online_set]


def release_context_devices() -> None:
    global _CONTEXT_DEVICES
    for serial in _CONTEXT_DEVICES or []:
        release_device_lock(serial)
        log_info(f"[{serial}] 已释放设备占用")
    _CONTEXT_DEVICES = None


def register_context_release() -> None:
    global _CONTEXT_RELEASE_REGISTERED
    if _CONTEXT_RELEASE_REGISTERED:
        return
    atexit.register(release_context_devices)
    _CONTEXT_RELEASE_REGISTERED = True


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
