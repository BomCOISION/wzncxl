from __future__ import annotations

import subprocess

from config import ADB_PATH
from common.log_utils import log_info


def run_adb_command(serial: str, args: list[str], check: bool = True) -> str:
    """执行 ADB 命令"""
    command = [str(ADB_PATH), "-s", serial, *args]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if check and result.returncode:
        raise RuntimeError(format_adb_error(serial, result))
    return result.stdout.strip()


def format_adb_error(serial: str, result: subprocess.CompletedProcess[str]) -> str:
    """格式化 ADB 错误"""
    error = result.stderr.strip() or result.stdout.strip() or "ADB 命令失败"
    return f"[{serial}] {error}"


def close_package(serial: str, package: str) -> None:
    """关闭应用包"""
    log_info(f"[{serial}] 关闭应用: {package}")
    run_adb_command(serial, ["shell", "am", "force-stop", package])


def get_package_pids(serial: str, package: str) -> list[str]:
    """获取应用进程 PID"""
    output = run_adb_command(serial, ["shell", "pidof", package], check=False)
    return output.split()


def resolve_launch_activity(serial: str, package: str, activity: str) -> str:
    """解析启动目标"""
    if activity:
        return format_activity_name(package, activity)
    return find_launcher_activity(serial, package)


def find_launcher_activity(serial: str, package: str) -> str:
    """查找启动 Activity"""
    args = ["shell", "cmd", "package", "resolve-activity", "--brief", package]
    output = run_adb_command(serial, args)
    return select_activity_line(serial, package, output.splitlines())


def select_activity_line(serial: str, package: str, lines: list[str]) -> str:
    """选择 Activity 输出行"""
    for line in reversed(lines):
        if match_activity_line(package, line.strip()):
            return line.strip()
    raise RuntimeError(f"[{serial}] 未找到启动 Activity: {package}")


def match_activity_line(package: str, line: str) -> bool:
    """判断是否为 Activity 行"""
    return line.startswith(f"{package}/") and len(line) > len(package) + 1


def format_activity_name(package: str, activity: str) -> str:
    """格式化 Activity 名称"""
    if "/" in activity:
        return activity
    return f"{package}/{activity}"


def start_activity(serial: str, target: str) -> None:
    """启动 Activity 或应用包"""
    log_info(f"[{serial}] 启动应用: {target}")
    start_named_activity(serial, target)


def start_named_activity(serial: str, target: str) -> None:
    """按 Activity 启动应用"""
    run_adb_command(serial, ["shell", "am", "start", "-n", target])
