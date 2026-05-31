from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
from typing import Any

from config import DEVICE_LOCK_STATE_PATH


def acquire_device_lock(candidates: list[str]) -> str:
    candidates = normalize_candidates(candidates)
    with locked_device_state():
        locks = cleanup_locks(read_locks())
        serial = pick_available_device(candidates, locks)
        locks[serial] = create_lock_entry()
        write_locks(locks)
        return serial


def release_device_lock(serial: str) -> None:
    with locked_device_state():
        locks = read_locks()
        remove_own_lock(locks, serial)
        write_locks(locks)


def normalize_candidates(candidates: list[str]) -> list[str]:
    unique: list[str] = []
    for serial in candidates:
        append_unique_serial(unique, str(serial).strip())
    return unique


def append_unique_serial(unique: list[str], serial: str) -> None:
    if serial and serial not in unique:
        unique.append(serial)


@contextmanager
def locked_device_state():
    lock_path = get_lock_path()
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as handle:
        lock_file(handle)
        try:
            yield
        finally:
            unlock_file(handle)


def get_lock_path() -> Path:
    return DEVICE_LOCK_STATE_PATH.with_name(DEVICE_LOCK_STATE_PATH.name + ".lock")


def lock_file(handle) -> None:
    handle.seek(0)
    if os.name == "nt":
        lock_file_windows(handle)
        return
    lock_file_unix(handle)


def unlock_file(handle) -> None:
    handle.seek(0)
    if os.name == "nt":
        unlock_file_windows(handle)
        return
    unlock_file_unix(handle)


def lock_file_windows(handle) -> None:
    import msvcrt
    msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)


def unlock_file_windows(handle) -> None:
    import msvcrt
    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def lock_file_unix(handle) -> None:
    import fcntl
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)


def unlock_file_unix(handle) -> None:
    import fcntl
    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def read_locks() -> dict[str, dict[str, Any]]:
    if not DEVICE_LOCK_STATE_PATH.exists():
        return {}
    return parse_locks(DEVICE_LOCK_STATE_PATH.read_text(encoding="utf-8"))


def parse_locks(text: str) -> dict[str, dict[str, Any]]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def write_locks(locks: dict[str, dict[str, Any]]) -> None:
    DEVICE_LOCK_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = DEVICE_LOCK_STATE_PATH.with_suffix(".tmp")
    temp_path.write_text(format_locks(locks), encoding="utf-8")
    temp_path.replace(DEVICE_LOCK_STATE_PATH)


def format_locks(locks: dict[str, dict[str, Any]]) -> str:
    return json.dumps(locks, ensure_ascii=False, indent=2)


def cleanup_locks(locks: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {serial: entry for serial, entry in locks.items() if is_lock_alive(entry)}


def is_lock_alive(entry: dict[str, Any]) -> bool:
    pid = get_lock_pid(entry)
    return pid is not None and is_process_alive(pid)


def get_lock_pid(entry: dict[str, Any]) -> int | None:
    try:
        return int(entry.get("pid"))
    except (TypeError, ValueError):
        return None


def is_process_alive(pid: int) -> bool:
    if os.name == "nt":
        return is_process_alive_windows(pid)
    return is_process_alive_unix(pid)


def is_process_alive_unix(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True
    except OSError:
        return False


def is_process_alive_windows(pid: int) -> bool:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.OpenProcess(0x1000, False, pid)
    if not handle:
        return False
    try:
        exit_code = ctypes.c_ulong()
        if not kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
            return False
        return exit_code.value == 259
    finally:
        kernel32.CloseHandle(handle)


def pick_available_device(candidates: list[str], locks: dict[str, dict[str, Any]]) -> str:
    for serial in candidates:
        if serial not in locks:
            return serial
    raise RuntimeError(f"没有空闲在线设备，可选设备: {candidates}")


def create_lock_entry() -> dict[str, Any]:
    return {
        "pid": os.getpid(),
        "started_at": datetime.now().isoformat(timespec="seconds"),
    }


def remove_own_lock(locks: dict[str, dict[str, Any]], serial: str) -> None:
    entry = locks.get(serial)
    if entry is not None and get_lock_pid(entry) == os.getpid():
        del locks[serial]
