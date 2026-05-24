from __future__ import annotations

from config import MAIN_RESTART_MAX_TIMES
from time import perf_counter

from common.failure_utils import save_failure_screenshot
from common.log_utils import log_error, log_info
from common.progress_state import get_current_account_from_bottom_index, has_remaining_accounts, reset_progress
from common.step_runner import StepFailedError, run_step
from steps.step_0001_关闭并启动游戏 import run as run_step_0001
from steps.step_0002_等待游戏加载到登录界面 import run as run_step_0002
from steps.step_0003_点击退出登录按钮 import run as run_step_0003
from steps.step_0004_点击协议同意按钮 import run as run_step_0004
from steps.step_0005_点击QQ的IOS好友玩按钮 import run as run_step_0005
from steps.step_0006_等待王者荣耀权限申请页面 import run as run_step_0006
from steps.step_0007_点击QQ授权切换账号按钮 import run as run_step_0007
from steps.step_0008_选择QQ账号 import run as run_step_0008
from steps.step_0009_点击QQ授权同意按钮 import run as run_step_0009
from steps.step_0010_点击QQ信息同意按钮 import run as run_step_0010
from steps.step_0011_点击换区按钮 import run as run_step_0011
from steps.step_0012_识别我的服务器数量 import run as run_step_0012
from steps.step_0013_选择区服 import run as run_step_0013
from steps.step_0014_点击开始游戏按钮 import run as run_step_0014
from steps.step_0018_清理大厅遮挡 import run as run_step_0018
from steps.step_0019_点击来农场干农活按钮 import run as run_step_0019
from steps.step_0020_等待农场加载完成 import run as run_step_0020
from steps.step_0021_移动到黄色帽子雕塑 import run as run_step_0021
from steps.step_0022_点击一键务农按钮 import run as run_step_0022
from steps.step_0023_随机点击收获页面中间 import run as run_step_0023
from steps.step_0024_点击农场返回按钮 import run as run_step_0024
from steps.step_0025_点击返回大厅按钮 import run as run_step_0025
from steps.step_0026_点击大厅设置按钮 import run as run_step_0026
from steps.step_0027_点击当前界面指定位置 import run as run_step_0027
from steps.step_0028_点击设置页退出登录按钮 import run as run_step_0028
from steps.step_0029_点击确认退出按钮 import run as run_step_0029
from steps.step_0030_最后等待 import run as run_step_0030


def main(start_time: float) -> None:
    """调度自动化流程"""
    log_info("主流程开始")
    run_step("step_0001 关闭并启动游戏", run_step_0001)
    run_step("step_0002 等待游戏加载到登录界面", run_step_0002)
    run_all_accounts()
    reset_progress()
    log_total_time("主流程结束", start_time)


def run_all_accounts() -> None:
    while has_remaining_accounts():
        run_account_login_steps()
        run_current_account_servers()


def run_account_login_steps() -> None:
    run_step("step_0003 点击退出登录按钮", run_step_0003)
    run_step("step_0004 点击协议同意按钮", run_step_0004)
    run_step("step_0005 点击 QQ 的 iOS 好友玩按钮", run_step_0005)
    run_step("step_0006 等待王者荣耀权限申请页面", run_step_0006)
    run_step("step_0007 点击 QQ 授权切换账号按钮", run_step_0007)
    run_step("step_0008 选择 QQ 账号", run_step_0008)
    run_step("step_0009 点击 QQ 授权同意按钮", run_step_0009)
    run_step("step_0010 点击 QQ 信息同意按钮", run_step_0010)


def run_current_account_servers() -> None:
    account_index = get_current_account_from_bottom_index()
    while is_still_current_account(account_index):
        run_server_cycle()


def is_still_current_account(account_index: int) -> bool:
    return has_remaining_accounts() and get_current_account_from_bottom_index() == account_index


def run_server_cycle() -> None:
    run_step("step_0011 点击换区按钮", run_step_0011)
    run_step("step_0012 识别我的服务器数量", run_step_0012)
    run_step("step_0013 选择区服", run_step_0013)
    run_step("step_0014 点击开始游戏按钮", run_step_0014)
    run_step("step_0018 清理大厅遮挡", run_step_0018)
    run_step("step_0019 点击来农场干农活按钮", run_step_0019)
    run_step("step_0020 等待农场加载完成", run_step_0020)
    run_step("step_0021 移动到黄色帽子雕塑", run_step_0021)
    run_step("step_0022 点击一键务农按钮", run_step_0022)
    run_step("step_0023 随机点击收获页面中间", run_step_0023)
    run_step("step_0024 点击农场返回按钮", run_step_0024)
    run_step("step_0025 点击返回大厅按钮", run_step_0025)
    run_step("step_0026 点击大厅设置按钮", run_step_0026)
    run_step("step_0027 点击当前界面指定位置", run_step_0027)
    run_step("step_0028 点击设置页退出登录按钮", run_step_0028)
    run_step("step_0029 点击确认退出按钮", run_step_0029)
    run_step("step_0030 最后等待", run_step_0030)


def log_total_time(message: str, start_time: float) -> None:
    log_info(f"{message}，总耗时 {perf_counter() - start_time:.2f} 秒")


def log_step_stop(exc: StepFailedError) -> None:
    screenshot_path = try_save_failure_screenshot()
    log_error(f"流程停止步骤: {exc.step_name}")
    log_error(f"失败原因: {exc.error}")
    log_error(f"失败截图: {screenshot_path}")


def try_save_failure_screenshot() -> str:
    try:
        return str(save_failure_screenshot())
    except Exception as exc:
        return f"保存失败: {exc}"


def run_main_with_restart() -> None:
    for attempt in range(1, MAIN_RESTART_MAX_TIMES + 1):
        if run_main_once(attempt):
            return
    log_error(f"主流程连续失败 {MAIN_RESTART_MAX_TIMES} 次，停止自动重启")


def run_main_once(attempt: int) -> bool:
    start = perf_counter()
    try:
        log_info(f"主流程第 {attempt}/{MAIN_RESTART_MAX_TIMES} 次运行")
        main(start)
        return True
    except StepFailedError as exc:
        handle_step_failed(start, exc)
        return False
    except Exception as exc:
        handle_main_failed(start, exc)
        return False


def handle_step_failed(start: float, exc: StepFailedError) -> None:
    log_total_time("主流程失败", start)
    log_step_stop(exc)


def handle_main_failed(start: float, exc: Exception) -> None:
    log_total_time("主流程失败", start)
    log_error(f"主流程执行失败: {exc}")


if __name__ == "__main__":
    run_main_with_restart()
