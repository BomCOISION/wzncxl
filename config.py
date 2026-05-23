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

# QQ 与 iOS 好友玩按钮点击坐标。
QQ_IOS_FRIEND_BUTTON_POINT = tuple(get_config_value("qq_ios_friend_button_point", [1178, 850]))

# 点击 QQ 与 iOS 好友玩按钮前等待秒数。
QQ_IOS_FRIEND_BUTTON_WAIT_SECONDS = float(get_config_value("qq_ios_friend_button_wait_seconds", 0.1))

# 权限申请页固定元素内部模板路径列表。
PERMISSION_PAGE_TEMPLATE_PATHS = [
    resolve_project_path(path)
    for path in get_config_value("permission_page_templates", [
        "resources/templates/permission_page_title_core.png",
        "resources/templates/permission_page_agree_button_core.png",
    ])
]

# 权限申请页模板至少达标数量。
PERMISSION_PAGE_REQUIRED_MATCHES = int(get_config_value("permission_page_required_matches", 2))

# 等待权限申请页超时时间。
PERMISSION_PAGE_TIMEOUT_SECONDS = float(get_config_value("permission_page_timeout_seconds", 15))

# 权限申请页等待步骤开始时保存的实时截图路径。
PERMISSION_PAGE_LIVE_SCREENSHOT_PATH = resolve_project_path(
    get_config_value("permission_page_live_screenshot_path", "logs/permission_page_live_screen.png")
)

# QQ 授权页切换账号按钮点击坐标。
QQ_SWITCH_ACCOUNT_BUTTON_POINT = tuple(get_config_value("qq_switch_account_button_point", [540, 1672]))

# 点击 QQ 授权页切换账号按钮前等待秒数。
QQ_SWITCH_ACCOUNT_BUTTON_WAIT_SECONDS = float(get_config_value("qq_switch_account_button_wait_seconds", 0.1))

# QQ 账号列表当前可选账号数量。
QQ_ACCOUNT_COUNT = int(get_config_value("qq_account_count", 7))

# QQ 账号列表第一个账号点击坐标。
QQ_FIRST_ACCOUNT_POINT = tuple(get_config_value("qq_first_account_point", [540, 820]))

# QQ 账号列表单个账号行高。
QQ_ACCOUNT_ROW_HEIGHT = int(get_config_value("qq_account_row_height", 162))

# QQ 账号列表从下往上选择第几个账号。
QQ_SELECT_ACCOUNT_FROM_BOTTOM_INDEX = int(get_config_value("qq_select_account_from_bottom_index", 1))

# 点击 QQ 账号列表账号前等待秒数。
QQ_ACCOUNT_SELECT_WAIT_SECONDS = float(get_config_value("qq_account_select_wait_seconds", 0.1))

# QQ 授权页同意按钮点击坐标。
QQ_AUTHORIZE_AGREE_BUTTON_POINT = tuple(get_config_value("qq_authorize_agree_button_point", [540, 1545]))

# 点击 QQ 授权页同意按钮前等待秒数。
QQ_AUTHORIZE_AGREE_BUTTON_WAIT_SECONDS = float(get_config_value("qq_authorize_agree_button_wait_seconds", 0.1))

# QQ 信息页同意按钮点击坐标。
QQ_INFO_AGREE_BUTTON_POINT = tuple(get_config_value("qq_info_agree_button_point", [540, 1545]))

# 点击 QQ 信息页同意按钮前等待秒数。
QQ_INFO_AGREE_BUTTON_WAIT_SECONDS = float(get_config_value("qq_info_agree_button_wait_seconds", 0.1))

# 登录后换区按钮点击坐标。
CHANGE_SERVER_BUTTON_POINT = tuple(get_config_value("change_server_button_point", [1238, 727]))

# 点击换区按钮前等待秒数。
CHANGE_SERVER_BUTTON_WAIT_SECONDS = float(get_config_value("change_server_button_wait_seconds", 3))

# 我的服务器列表状态图标模板路径列表。
MY_SERVER_STATUS_TEMPLATE_PATHS = [
    resolve_project_path(path)
    for path in get_config_value("my_server_status_templates", [
        "resources/templates/server_status_red_core.png",
        "resources/templates/server_status_green_core.png",
    ])
]

# 我的服务器列表识别区域，格式为 x, y, 宽, 高。
MY_SERVER_LIST_REGION = tuple(get_config_value("my_server_list_region", [230, 220, 1660, 820]))

# 服务器状态图标模板匹配阈值。
SERVER_STATUS_MATCH_THRESHOLD = float(get_config_value("server_status_match_threshold", 0.82))

# 服务器状态图标去重距离。
SERVER_STATUS_DEDUP_DISTANCE = int(get_config_value("server_status_dedup_distance", 40))

# 服务器列表按从上到下、从左到右选择第几个区。
SERVER_SELECT_INDEX = int(get_config_value("server_select_index", 1))

# 从状态图标中心偏移到区服条目可点击位置。
SERVER_SELECT_POINT_OFFSET = tuple(get_config_value("server_select_point_offset", [220, 0]))

# 点击区服前等待秒数。
SERVER_SELECT_WAIT_SECONDS = float(get_config_value("server_select_wait_seconds", 0.1))

# 开始游戏按钮点击坐标。
START_GAME_BUTTON_POINT = tuple(get_config_value("start_game_button_point", [956, 839]))

# 点击开始游戏按钮前等待秒数。
START_GAME_BUTTON_WAIT_SECONDS = float(get_config_value("start_game_button_wait_seconds", 3))

# 弹窗关闭 X 模板路径。
POPUP_CLOSE_X_TEMPLATE_PATH = resolve_project_path(
    get_config_value("popup_close_x_template", "resources/templates/popup_close_x_core.png")
)

# 弹窗关闭 X 模板匹配阈值。
POPUP_CLOSE_X_MATCH_THRESHOLD = float(get_config_value("popup_close_x_match_threshold", 0.82))

# 识别弹窗关闭按钮前等待秒数。
POPUP_CLOSE_WAIT_SECONDS = float(get_config_value("popup_close_wait_seconds", 0.1))

# 干净大厅固定元素内部模板路径列表。
LOBBY_CLEAN_TEMPLATE_PATHS = [
    resolve_project_path(path)
    for path in get_config_value("lobby_clean_templates", [
        "resources/templates/lobby_settings_icon_core.png",
        "resources/templates/lobby_mail_icon_core.png",
        "resources/templates/lobby_bag_icon_core.png",
        "resources/templates/lobby_rank_text_core.png",
        "resources/templates/lobby_battle_text_core.png",
    ])
]

# 干净大厅模板至少达标数量。
LOBBY_CLEAN_REQUIRED_MATCHES = int(get_config_value("lobby_clean_required_matches", 3))

# 等待干净大厅超时时间。
LOBBY_CLEAN_TIMEOUT_SECONDS = float(get_config_value("lobby_clean_timeout_seconds", 8))

# 干净大厅连续稳定命中次数。
LOBBY_CLEAN_STABLE_HITS = int(get_config_value("lobby_clean_stable_hits", 2))

# 活动页返回按钮模板路径。
ACTIVITY_BACK_BUTTON_TEMPLATE_PATH = resolve_project_path(
    get_config_value("activity_back_button_template", "resources/templates/activity_back_button_core.png")
)

# 活动页返回按钮模板匹配阈值。
ACTIVITY_BACK_BUTTON_MATCH_THRESHOLD = float(get_config_value("activity_back_button_match_threshold", 0.82))

# 识别活动页返回按钮前等待秒数。
ACTIVITY_BACK_BUTTON_WAIT_SECONDS = float(get_config_value("activity_back_button_wait_seconds", 0.1))

# 清理大厅遮挡后再次判断前等待秒数。
LOBBY_CLEAR_RECHECK_WAIT_SECONDS = float(get_config_value("lobby_clear_recheck_wait_seconds", 2))

# 清理大厅遮挡最多循环次数。
LOBBY_CLEAR_MAX_ROUNDS = int(get_config_value("lobby_clear_max_rounds", 8))

# 来农场干农活按钮点击坐标。
FARM_WORK_BUTTON_POINT = tuple(get_config_value("farm_work_button_point", [598, 706]))

# 点击来农场干农活按钮前等待秒数。
FARM_WORK_BUTTON_WAIT_SECONDS = float(get_config_value("farm_work_button_wait_seconds", 0.1))

# 农场加载完成固定元素内部模板路径列表。
FARM_LOADED_TEMPLATE_PATHS = [
    resolve_project_path(path)
    for path in get_config_value("farm_loaded_templates", [
        "resources/templates/farm_rank_5v5_icon_core.png",
        "resources/templates/farm_warehouse_icon_core.png",
        "resources/templates/farm_social_icon_core.png",
        "resources/templates/farm_action_icon_core.png",
        "resources/templates/farm_duo_action_icon_core.png",
    ])
]

# 农场加载完成模板至少达标数量。
FARM_LOADED_REQUIRED_MATCHES = int(get_config_value("farm_loaded_required_matches", 3))

# 等待农场加载完成超时时间。
FARM_LOADED_TIMEOUT_SECONDS = float(get_config_value("farm_loaded_timeout_seconds", 30))

# 农场加载完成连续稳定命中次数。
FARM_LOADED_STABLE_HITS = int(get_config_value("farm_loaded_stable_hits", 2))

# 农场方向键中心坐标。
FARM_JOYSTICK_CENTER_POINT = tuple(get_config_value("farm_joystick_center_point", [288, 765]))

# 农场向左上角奔跑滑动终点坐标。
FARM_RUN_LEFT_UP_END_POINT = tuple(get_config_value("farm_run_left_up_end_point", [190, 625]))

# 农场向黄色帽子雕塑移动持续时间毫秒。
FARM_RUN_TO_HAT_STATUE_DURATION_MS = int(get_config_value("farm_run_to_hat_statue_duration_ms", 2900))

# 一键务农按钮点击坐标。
ONE_CLICK_FARM_BUTTON_POINT = tuple(get_config_value("one_click_farm_button_point", [1284, 631]))

# 点击一键务农按钮前等待秒数。
ONE_CLICK_FARM_BUTTON_WAIT_SECONDS = float(get_config_value("one_click_farm_button_wait_seconds", 0.1))

# 收获页面出现前等待秒数。
HARVEST_PAGE_WAIT_SECONDS = float(get_config_value("harvest_page_wait_seconds", 5))

# 收获页面随机点击屏幕中间区域，格式为 x, y, 宽, 高。
HARVEST_RANDOM_TAP_REGION = tuple(get_config_value("harvest_random_tap_region", [760, 390, 400, 300]))

# 农场左上角返回按钮点击坐标。
FARM_BACK_BUTTON_POINT = tuple(get_config_value("farm_back_button_point", [108, 57]))

# 点击农场返回按钮前等待秒数。
FARM_BACK_BUTTON_WAIT_SECONDS = float(get_config_value("farm_back_button_wait_seconds", 0.5))

# 返回大厅按钮点击坐标。
BACK_TO_LOBBY_BUTTON_POINT = tuple(get_config_value("back_to_lobby_button_point", [1158, 759]))

# 点击返回大厅按钮前等待秒数。
BACK_TO_LOBBY_BUTTON_WAIT_SECONDS = float(get_config_value("back_to_lobby_button_wait_seconds", 1))

# 大厅右上角设置按钮点击坐标。
LOBBY_SETTINGS_BUTTON_POINT = tuple(get_config_value("lobby_settings_button_point", [1762, 59]))

# 点击大厅设置按钮前等待秒数。
LOBBY_SETTINGS_BUTTON_WAIT_SECONDS = float(get_config_value("lobby_settings_button_wait_seconds", 5))

# 当前界面指定位置点击坐标。
CURRENT_INTERFACE_CLICK_POINT = tuple(get_config_value("current_interface_click_point", [872, 857]))

# 点击当前界面指定位置前等待秒数。
CURRENT_INTERFACE_CLICK_WAIT_SECONDS = float(get_config_value("current_interface_click_wait_seconds", 1))

# 设置页退出登录按钮点击坐标。
SETTINGS_LOGOUT_BUTTON_POINT = tuple(get_config_value("settings_logout_button_point", [1631, 923]))

# 点击设置页退出登录按钮前等待秒数。
SETTINGS_LOGOUT_BUTTON_WAIT_SECONDS = float(get_config_value("settings_logout_button_wait_seconds", 0.5))

# 确认退出按钮点击坐标。
LOGOUT_CONFIRM_BUTTON_POINT = tuple(get_config_value("logout_confirm_button_point", [1147, 766]))

# 点击确认退出按钮前等待秒数。
LOGOUT_CONFIRM_BUTTON_WAIT_SECONDS = float(get_config_value("logout_confirm_button_wait_seconds", 1))

# 最后等待秒数。
FINAL_WAIT_SECONDS = float(get_config_value("final_wait_seconds", 10))

# 自动化进度状态保存路径。
PROGRESS_STATE_PATH = resolve_project_path(get_config_value("progress_state_path", "logs/progress_state.json"))

# 失败时固定截图保存路径。
FAILURE_SCREENSHOT_PATH = resolve_project_path(get_config_value("failure_screenshot_path", "logs/failure_screen.png"))
