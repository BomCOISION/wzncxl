from __future__ import annotations

from ast import literal_eval
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parent
CONFIG_YAML = PROJECT_DIR / "config.yaml"


def parse_config_value(raw_value: str) -> Any:
    """解析 config.yaml 中的简单配置值"""
    raw_value = raw_value.strip()
    if not raw_value:
        return ""
    try:
        return literal_eval(raw_value)
    except (SyntaxError, ValueError):
        return raw_value.strip("\"'")


def load_config_line(data: dict[str, Any], line: str) -> None:
    """读取单行配置"""
    row = line.split("#", 1)[0].strip()
    if not row or ":" not in row:
        return
    key, value = row.split(":", 1)
    data[key.strip()] = parse_config_value(value)


def load_config_data() -> dict[str, Any]:
    """读取项目配置"""
    data: dict[str, Any] = {}
    if not CONFIG_YAML.exists():
        return data
    for line in CONFIG_YAML.read_text(encoding="utf-8").splitlines():
        load_config_line(data, line)
    return data


def get_config_value(name: str, default: Any) -> Any:
    """获取配置值"""
    return CONFIG_DATA.get(name, default)


def get_target_devices() -> list[str]:
    """获取目标设备列表"""
    devices = get_config_value("target_devices", None)
    if devices:
        return [str(device) for device in devices]
    serial = str(get_config_value("device_serial", "")).strip()
    return [serial] if serial else []


def resolve_project_path(value: Any) -> Path:
    """解析项目相对路径"""
    path = Path(str(value))
    if path.is_absolute():
        return path
    return PROJECT_DIR / path


CONFIG_DATA = load_config_data()

# ADB 可执行文件路径。
ADB_PATH = Path(str(get_config_value("adb_path", "adb")))

# 目标设备序列号列表。
TARGET_DEVICES = get_target_devices()

# 王者荣耀 Android 包名。
KING_PACKAGE = str(get_config_value("king_package", "com.tencent.tmgp.sgame"))

# 王者荣耀启动 Activity；为空时按包名启动。
KING_ACTIVITY = str(get_config_value("king_activity", "")).strip()

# 启动后等待游戏进程出现的秒数。
STARTUP_WAIT_SECONDS = float(get_config_value("startup_wait_seconds", 15))

# ADB 命令超时时间。
ADB_COMMAND_TIMEOUT_SECONDS = float(get_config_value("adb_command_timeout_seconds", 30))

# 步骤重试次数。
RETRY_TIMES = int(get_config_value("retry_times", 1))

# 登录页固定图标内部模板路径列表。
LOGIN_PAGE_TEMPLATE_PATHS = [
    resolve_project_path(path)
    for path in get_config_value("login_page_templates", [
        "resources/templates/login_exit_button_core.png",
        "resources/templates/login_start_button_core.png",
        "resources/templates/login_upload_log_icon_core.png",
    ])
]

# 登录页模板至少达标数量。
LOGIN_PAGE_REQUIRED_MATCHES = int(get_config_value("login_page_required_matches", 2))

# 每次识别连续截图帧数。
SCREENSHOT_MEDIAN_FRAME_COUNT = int(get_config_value("screenshot_median_frame_count", 5))

# 模板匹配通过阈值。
TEMPLATE_MATCH_THRESHOLD = float(get_config_value("template_match_threshold", 0.82))

# 连续稳定命中次数。
TEMPLATE_STABLE_HITS = int(get_config_value("template_stable_hits", 3))

# 等待登录界面超时时间。
GAME_LOAD_TIMEOUT_SECONDS = float(get_config_value("game_load_timeout_seconds", 90))

# 每轮页面识别间隔时间。
TEMPLATE_MATCH_INTERVAL_SECONDS = float(get_config_value("template_match_interval_seconds", 0.8))

# 登录页右上角退出按钮点击坐标。
LOGIN_EXIT_BUTTON_POINT = tuple(get_config_value("login_exit_button_point", [1833, 43]))

# 协议弹窗同意按钮点击坐标。
AGREEMENT_AGREE_BUTTON_POINT = tuple(get_config_value("agreement_agree_button_point", [1147, 819]))

# 点击协议同意按钮前等待秒数。
AGREEMENT_AGREE_WAIT_SECONDS = float(get_config_value("agreement_agree_wait_seconds", 0.2))
