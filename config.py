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

# 是否显式配置多设备列表。
TARGET_DEVICE_LIST_CONFIGURED = get_config_value("target_devices", None) is not None

# 当前被脚本占用的设备记录文件。
DEVICE_LOCK_STATE_PATH = resolve_project_path(
    get_config_value("device_lock_state_path", "C:\\Users\\18099\\Desktop\\Items\\device_locks.json")
)

# 模拟器分辨率。
SCREEN_RESOLUTION = tuple(get_config_value("resolution", [1080, 1920]))

# 王者荣耀 Android 包名。
KING_PACKAGE = "com.tencent.tmgp.sgame"

# 王者荣耀启动 Activity；为空时按包名启动。
KING_ACTIVITY = ""

# 步骤重试次数。
RETRY_TIMES = 1

# 主流程失败后最多自动重启次数。
MAIN_RESTART_MAX_TIMES = 1000

# 启用的扩展流程列表；为空时不执行任何扩展。
ENABLED_EXTENSIONS = [str(name) for name in get_config_value("enabled_extensions", [])]

# 登录页固定图标内部模板路径列表。
LOGIN_PAGE_TEMPLATE_PATHS = [
    resolve_project_path("resources/templates/login_exit_button_core.png"),
    resolve_project_path("resources/templates/login_start_button_core.png"),
    resolve_project_path("resources/templates/login_upload_log_icon_core.png"),
]

# 登录页模板匹配区域映射，格式为 模板文件名: [x, y, 宽, 高]。
LOGIN_PAGE_TEMPLATE_REGIONS = {
    "login_exit_button_core": (1760, 0, 150, 110),
    "login_start_button_core": (780, 740, 360, 160),
    "login_upload_log_icon_core": (1780, 500, 120, 140),
}

# 登录页右上角退出按钮点击坐标。
LOGIN_EXIT_BUTTON_POINT = (1833, 43)

# 登录页公告弹窗右上角关闭按钮点击坐标。
LOGIN_NOTICE_CLOSE_BUTTON_POINT = (1633, 148)

# 协议弹窗同意按钮点击坐标。
AGREEMENT_AGREE_BUTTON_POINT = (1147, 819)

# QQ 与 iOS 好友玩按钮点击坐标。
QQ_IOS_FRIEND_BUTTON_POINT = (1178, 850)

# 权限申请页固定元素内部模板路径列表。
PERMISSION_PAGE_TEMPLATE_PATHS = [
    resolve_project_path("resources/templates/permission_page_title_core.png"),
    resolve_project_path("resources/templates/permission_page_agree_button_core.png"),
]

# 权限申请页等待步骤开始时保存的实时截图路径。
PERMISSION_PAGE_LIVE_SCREENSHOT_PATH = resolve_project_path("logs/permission_page_live_screen.png")

# QQ 授权页切换账号按钮点击坐标。
QQ_SWITCH_ACCOUNT_BUTTON_POINT = (540, 1672)

# QQ 账号列表当前可选账号数量。
QQ_ACCOUNT_COUNT = 7

# QQ 账号列表第一个账号点击坐标。
QQ_FIRST_ACCOUNT_POINT = (540, 820)

# QQ 账号列表单个账号行高。
QQ_ACCOUNT_ROW_HEIGHT = 162

# QQ 账号列表从下往上选择第几个账号。
QQ_SELECT_ACCOUNT_FROM_BOTTOM_INDEX = 1

# QQ 授权页同意按钮点击坐标。
QQ_AUTHORIZE_AGREE_BUTTON_POINT = (540, 1545)

# QQ 信息页同意按钮点击坐标。
QQ_INFO_AGREE_BUTTON_POINT = (540, 1545)

# 登录后换区按钮点击坐标。
CHANGE_SERVER_BUTTON_POINT = (1238, 727)

# 我的服务器列表状态图标模板路径列表。
MY_SERVER_STATUS_TEMPLATE_PATHS = [
    resolve_project_path("resources/templates/server_status_red_core.png"),
    resolve_project_path("resources/templates/server_status_green_core.png"),
]

# 我的服务器列表识别区域，格式为 x, y, 宽, 高。
MY_SERVER_LIST_REGION = (230, 220, 1660, 820)

# 服务器列表按从上到下、从左到右选择第几个区。
SERVER_SELECT_INDEX = 1

# 从状态图标中心偏移到区服条目可点击位置。
SERVER_SELECT_POINT_OFFSET = (220, 0)

# 开始游戏按钮点击坐标。
START_GAME_BUTTON_POINT = (956, 839)

# 弹窗关闭 X 模板路径。
POPUP_CLOSE_X_TEMPLATE_PATH = resolve_project_path("resources/templates/popup_close_x_core.png")

# 弹窗关闭 X 模板匹配区域，格式为 x, y, 宽, 高。
POPUP_CLOSE_X_MATCH_REGION = (1450, 40, 460, 220)

# 干净大厅固定元素内部模板路径列表。
LOBBY_CLEAN_TEMPLATE_PATHS = [
    resolve_project_path("resources/templates/lobby_settings_icon_core.png"),
    resolve_project_path("resources/templates/lobby_mail_icon_core.png"),
    resolve_project_path("resources/templates/lobby_bag_icon_core.png"),
    resolve_project_path("resources/templates/lobby_rank_text_core.png"),
    resolve_project_path("resources/templates/lobby_battle_text_core.png"),
]

# 干净大厅模板匹配区域映射，格式为 模板文件名: [x, y, 宽, 高]。
LOBBY_CLEAN_TEMPLATE_REGIONS = {
    "lobby_settings_icon_core": (1690, 20, 150, 110),
    "lobby_mail_icon_core": (1600, 25, 130, 100),
    "lobby_bag_icon_core": (1430, 950, 150, 100),
    "lobby_rank_text_core": (1030, 740, 260, 150),
    "lobby_battle_text_core": (630, 740, 260, 150),
}

# 活动页返回按钮模板路径。
ACTIVITY_BACK_BUTTON_TEMPLATE_PATH = resolve_project_path("resources/templates/activity_back_button_core.png")

# 活动页返回按钮模板匹配区域，格式为 x, y, 宽, 高。
ACTIVITY_BACK_BUTTON_MATCH_REGION = (0, 0, 260, 150)

# 清理大厅遮挡最多循环次数。
LOBBY_CLEAR_MAX_ROUNDS = 18

# 来农场干农活按钮点击坐标。
FARM_WORK_BUTTON_POINT = (598, 706)

# 农场加载完成固定元素内部模板路径列表。
FARM_LOADED_TEMPLATE_PATHS = [
    resolve_project_path("resources/templates/farm_rank_5v5_icon_core.png"),
    resolve_project_path("resources/templates/farm_warehouse_icon_core.png"),
    resolve_project_path("resources/templates/farm_social_icon_core.png"),
    resolve_project_path("resources/templates/farm_action_icon_core.png"),
    resolve_project_path("resources/templates/farm_duo_action_icon_core.png"),
]

# 农场加载完成模板匹配区域映射，格式为 模板文件名: [x, y, 宽, 高]。
FARM_LOADED_TEMPLATE_REGIONS = {
    "farm_rank_5v5_icon_core": (1560, 20, 310, 100),
    "farm_warehouse_icon_core": (1780, 160, 120, 120),
    "farm_social_icon_core": (1780, 260, 120, 130),
    "farm_action_icon_core": (1300, 800, 180, 150),
    "farm_duo_action_icon_core": (1280, 570, 220, 180),
}

# 农场未加载完成时点击的活动页返回按钮固定坐标。
FARM_LOADED_ACTIVITY_BACK_BUTTON_POINT = (100, 63)

# 农场返回弹窗右上角关闭按钮固定坐标。
FARM_LOADED_BACK_POPUP_CLOSE_POINT = (1415, 273)

# 农场升级箭头内部模板路径。
FARM_UPGRADE_ARROW_TEMPLATE_PATH = resolve_project_path("resources/templates/farm_upgrade_arrow_core.png")

# 农场升级箭头模板匹配区域，格式为 x, y, 宽, 高。
FARM_UPGRADE_ARROW_MATCH_REGION = (300, 45, 280, 80)

# 农场升级判断时保存的当前截图路径。
FARM_UPGRADE_SCAN_SCREENSHOT_PATH = resolve_project_path("logs/farm_upgrade_scan_screen.png")

# 农场升级判断结果保存路径。
FARM_UPGRADE_RESULT_PATH = resolve_project_path("logs/farm_upgrade_result.json")

# 农场升级箭头固定点击坐标。
FARM_UPGRADE_ARROW_CLICK_POINT = (448, 75)

# 农场升级界面右下角升级按钮固定点击坐标。
FARM_UPGRADE_BUTTON_POINT = (1553, 981)

# 首次点击升级按钮后继续重复点击升级按钮次数。
FARM_UPGRADE_REPEAT_CLICK_TIMES = 6

# 农场升级界面左上角返回按钮固定点击坐标。
FARM_UPGRADE_BACK_BUTTON_POINT = (100, 63)

# 仓库按钮固定点击坐标。
SELL_WAREHOUSE_BUTTON_POINT = (1832, 220)

# 仓库界面批量出售按钮固定点击坐标。
SELL_WAREHOUSE_BATCH_SELL_BUTTON_POINT = (1388, 972)

# 批量出售界面选择全部选项框固定点击坐标。
SELL_WAREHOUSE_SELECT_ALL_POINT = (1048, 892)

# 批量出售界面出售按钮固定点击坐标。
SELL_WAREHOUSE_CONFIRM_SELL_BUTTON_POINT = (1532, 971)

# 仓库界面右上角关闭按钮固定点击坐标。
SELL_WAREHOUSE_CLOSE_BUTTON_POINT = (1778, 94)

# 开土地流程中农场右下角还原位置按钮固定点击坐标。
OPEN_LAND_RESTORE_BUTTON_POINT = (1779, 980)

# 开土地正前方奔跑时摇杆拖动终点坐标。
OPEN_LAND_FORWARD_END_POINT = (288, 625)

# 开土地正左方移动时摇杆拖动终点坐标。
OPEN_LAND_LEFT_END_POINT = (148, 765)

# 开土地界面开垦按钮固定点击坐标。
OPEN_LAND_CULTIVATE_BUTTON_POINT = (1283, 617)

# 开土地确认弹窗确定按钮固定点击坐标。
OPEN_LAND_CONFIRM_BUTTON_POINT = (1159, 758)

# 开土地确认后取消按钮固定点击坐标。
OPEN_LAND_CANCEL_BUTTON_POINT = (761, 758)

# 开土地等级不够弹窗右上角 X 固定点击坐标。
OPEN_LAND_LEVEL_NOT_ENOUGH_CLOSE_POINT = (1415, 273)

# 开土地当前一行需要开垦的土地数量。
OPEN_LAND_ROW_LAND_COUNT = 4

# 开土地第二行向右移动时摇杆拖动终点坐标。
OPEN_LAND_RIGHT_END_POINT = (428, 765)

# 开土地到下一行时正前方移动的摇杆拖动终点坐标。
OPEN_LAND_NEXT_ROW_FORWARD_END_POINT = (288, 625)

# 开土地第二行完成第 5 块后继续向右开垦的土地数量。
OPEN_LAND_SECOND_ROW_RIGHT_COUNT = 3

# 开土地第三行完成第 9 块后继续向左开垦的土地数量。
OPEN_LAND_THIRD_ROW_LEFT_COUNT = 3

# 当前界面右下角种植按钮 X 键点击坐标。
CHANGE_CROP_DELETE_X_BUTTON_POINT = (1716, 779)

# 当前界面右下角种植按钮点击坐标。
CHANGE_CROP_PLANT_BUTTON_POINT = (1622, 865)

# 打开作物列表后固定点击的第一个农作物坐标。
CHANGE_CROP_FIRST_CROP_POINT = (1095, 221)

# 作物列表选择按钮点击坐标。
CHANGE_CROP_SELECT_BUTTON_POINT = (1355, 970)

# 作物列表识别时保存的当前截图路径。
CROP_LIST_SCAN_SCREENSHOT_PATH = resolve_project_path("logs/crop_list_scan_screen.png")

# 作物列表识别结果保存路径。
CROP_LIST_RESULT_PATH = resolve_project_path("logs/crop_list_scan_result.json")

# 作物列表时间文字模板匹配区域，格式为 x, y, 宽, 高。
CROP_LIST_MATCH_REGION = (1000, 140, 700, 740)

# 作物列表时间文字模板匹配结果图路径。
CROP_LIST_MATCH_RESULT_IMAGE_PATH = resolve_project_path("logs/crop_list_match_result.png")

# 用来选择目标作物的成熟时间。
CROP_LIST_TARGET_CROP_TIME = "32小时"

# 从时间文字中心偏移到作物图标中心的坐标。
CROP_LIST_TIME_TO_ICON_OFFSET = (0, -65)

# 作物优先级分组；1 组优先辣椒再卷心菜再蓝莓，2 组优先西瓜再柚子再香蕉，3 组优先草莓。
CROP_ICON_PRIORITY_GROUPS = {
    1: ["辣椒", "卷心菜", "蓝莓"],
    2: ["西瓜", "柚子", "香蕉"],
    3: ["草莓"],
}

# 作物图标模板路径映射。
CROP_ICON_TEMPLATE_PATHS = {
    "辣椒": resolve_project_path("resources/templates/crop_icon_chili_core.png"),
    "卷心菜": resolve_project_path("resources/templates/crop_icon_cabbage_core.png"),
    "蓝莓": resolve_project_path("resources/templates/crop_icon_blueberry_core.png"),
    "西瓜": resolve_project_path("resources/templates/crop_icon_watermelon_core.png"),
    "柚子": resolve_project_path("resources/templates/crop_icon_grapefruit_core.png"),
    "香蕉": resolve_project_path("resources/templates/crop_icon_banana_core.png"),
    "草莓": resolve_project_path("resources/templates/crop_icon_strawberry_core.png"),
}

# 作物列表时间文字模板路径映射。
CROP_LIST_TIME_TEMPLATE_PATHS = {
    "30秒": resolve_project_path("resources/templates/crop_time_30s_text_core.png"),
    "2分钟": resolve_project_path("resources/templates/crop_time_2m_text_core.png"),
    "5分钟": resolve_project_path("resources/templates/crop_time_5m_text_core.png"),
    "20分钟": resolve_project_path("resources/templates/crop_time_20m_text_core.png"),
    "1小时": resolve_project_path("resources/templates/crop_time_1h_text_core.png"),
    "8小时": resolve_project_path("resources/templates/crop_time_8h_text_core.png"),
    "16小时": resolve_project_path("resources/templates/crop_time_16h_text_core.png"),
    "32小时": resolve_project_path("resources/templates/crop_time_32h_text_core.png"),
}

# 农场方向键中心坐标。
FARM_JOYSTICK_CENTER_POINT = (288, 765)

# 农场向左上角奔跑滑动终点坐标。
FARM_RUN_LEFT_UP_END_POINT = (190, 625)

# 一键务农按钮点击坐标。
ONE_CLICK_FARM_BUTTON_POINT = (1284, 631)

# 祝福好友流程右下角还原按钮点击坐标。
BLESS_FRIENDS_RESTORE_BUTTON_POINT = (1779, 980)

# 祝福好友流程右侧社交图标点击坐标。
BLESS_FRIENDS_SOCIAL_BUTTON_POINT = (1832, 331)

# 祝福好友流程右侧第一个好友拜访按钮点击坐标。
BLESS_FRIENDS_FIRST_VISIT_BUTTON_POINT = (1832, 188)

# 到达好友土地后祝福按钮点击坐标。
BLESS_FRIENDS_WISH_BUTTON_POINT = (1609, 593)

# 好友农场右上角回家按钮点击坐标。
BLESS_FRIENDS_HOME_BUTTON_POINT = (1746, 60)

# 祝福好友每日目标祝福次数。
BLESS_FRIENDS_TARGET_COUNT = 10

# 祝福好友候选土地编号列表，1-12 为左侧土地，13-24 为右侧土地。
BLESS_FRIENDS_LAND_INDEXES = [
    int(land_index)
    for land_index in get_config_value("bless_friends_land_indexes", list(range(1, 25)))
]

# 祝福次数 3/3 模板路径，用于判断当前土地祝福次数已满。
BLESS_FRIENDS_FULL_COUNT_TEMPLATE_PATH = resolve_project_path("resources/templates/bless_count_3_3_core.png")

# 祝福次数 3/3 模板匹配区域，格式为 [x, y, 宽, 高]。
BLESS_FRIENDS_FULL_COUNT_MATCH_REGION = (230, 290, 95, 90)

# 祝福次数识别时保存的当前截图路径。
BLESS_FRIENDS_FULL_COUNT_SCAN_SCREENSHOT_PATH = resolve_project_path("logs/bless_friends_full_count_scan.png")

# 置顶好友流程右下角还原按钮点击坐标。
PIN_FRIEND_RESTORE_BUTTON_POINT = (1779, 980)

# 置顶好友流程右侧社交图标点击坐标。
PIN_FRIEND_SOCIAL_BUTTON_POINT = (1832, 331)

# 置顶好友头像内部模板路径。
PIN_FRIEND_AVATAR_TEMPLATE_PATH = resolve_project_path("resources/templates/pin_friend_avatar_core.png")

# 置顶好友头像模板匹配区域，格式为 [x, y, 宽, 高]。
PIN_FRIEND_AVATAR_MATCH_REGION = (1070, 145, 110, 820)

# 置顶好友头像识别时保存的当前截图路径。
PIN_FRIEND_AVATAR_SCAN_SCREENSHOT_PATH = resolve_project_path("logs/pin_friend_avatar_scan.png")

# 置顶好友列表第一个头像中心 Y 坐标。
PIN_FRIEND_FIRST_AVATAR_CENTER_Y = 197

# 置顶好友列表单行高度。
PIN_FRIEND_ROW_HEIGHT = 159

# 置顶好友同一行右侧更多按钮中心 X 坐标。
PIN_FRIEND_MORE_BUTTON_X = 1748

# 从置顶好友头像中心 Y 偏移到更多按钮中心 Y 的坐标。
PIN_FRIEND_MORE_BUTTON_Y_OFFSET = 0

# 收获页面点击继续文本坐标。
HARVEST_CONTINUE_TEXT_POINT = (1260, 964)

# 农场左上角返回按钮点击坐标。
FARM_BACK_BUTTON_POINT = (108, 57)

# 返回大厅按钮点击坐标。
BACK_TO_LOBBY_BUTTON_POINT = (1158, 759)

# 大厅右上角设置按钮点击坐标。
LOBBY_SETTINGS_BUTTON_POINT = (1762, 59)

# 当前界面指定位置点击坐标。
CURRENT_INTERFACE_CLICK_POINT = (872, 857)

# 设置页退出登录按钮点击坐标。
SETTINGS_LOGOUT_BUTTON_POINT = (1631, 923)

# 确认退出按钮点击坐标。
LOGOUT_CONFIRM_BUTTON_POINT = (1147, 766)

# 自动化进度状态保存路径。
PROGRESS_STATE_PATH = resolve_project_path("config/progress_state.json")

# 失败时固定截图保存路径。
FAILURE_SCREENSHOT_PATH = resolve_project_path("config/failure_screen.png")
