from __future__ import annotations

from config import ADB_PATH, KING_ACTIVITY, KING_PACKAGE, STARTUP_WAIT_SECONDS
from common.log_utils import log_info
from common.process_utils import close_package, get_package_pids, resolve_launch_activity, start_activity
from common.run_context import get_context_devices
from common.wait_utils import wait_seconds


def run() -> None:
    """执行关闭并启动游戏步骤"""
    check_config()
    restart_game_on_devices(get_context_devices())


def check_config() -> None:
    """检查基础配置"""
    if str(ADB_PATH) != "adb" and not ADB_PATH.exists():
        raise FileNotFoundError(f"ADB 不存在: {ADB_PATH}")


def restart_game_on_devices(devices: list[str]) -> None:
    """逐个设备重启游戏"""
    for serial in devices:
        restart_game(serial)


def restart_game(serial: str) -> None:
    """关闭并启动单个设备上的游戏"""
    old_pids = close_game(serial)
    start_game(serial)
    new_pids = wait_for_game_started(serial)
    log_restart_result(serial, old_pids, new_pids)


def close_game(serial: str) -> list[str]:
    """关闭游戏并返回旧进程"""
    old_pids = get_package_pids(serial, KING_PACKAGE)
    close_package(serial, KING_PACKAGE)
    check_game_closed(serial)
    return old_pids


def check_game_closed(serial: str) -> None:
    """检查游戏是否已经关闭"""
    pids = get_package_pids(serial, KING_PACKAGE)
    if pids:
        raise RuntimeError(f"[{serial}] 游戏关闭失败: {pids}")


def start_game(serial: str) -> None:
    """启动游戏"""
    activity = resolve_launch_activity(serial, KING_PACKAGE, KING_ACTIVITY)
    start_activity(serial, activity)


def wait_for_game_started(serial: str) -> list[str]:
    """等待游戏进程启动"""
    wait_seconds(STARTUP_WAIT_SECONDS)
    pids = get_package_pids(serial, KING_PACKAGE)
    if not pids:
        raise RuntimeError(f"[{serial}] 游戏启动后未发现进程")
    return pids


def log_restart_result(serial: str, old_pids: list[str], new_pids: list[str]) -> None:
    """记录重启结果"""
    if old_pids:
        log_info(f"[{serial}] 已关闭旧进程: {old_pids}")
    else:
        log_info(f"[{serial}] 启动前未发现游戏进程")
    log_info(f"[{serial}] 已启动游戏进程: {new_pids}")
