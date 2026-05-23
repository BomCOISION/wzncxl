from __future__ import annotations

from time import perf_counter

from common.log_utils import log_exception, log_info
from common.step_runner import run_step
from steps.step_0001_关闭并启动游戏 import run as run_step_0001
from steps.step_0002_等待游戏加载到登录界面 import run as run_step_0002
from steps.step_0003_点击退出登录按钮 import run as run_step_0003
from steps.step_0004_点击协议同意按钮 import run as run_step_0004


def main(start_time: float) -> None:
    """调度自动化流程"""
    log_info("主流程开始")
    run_step("step_0001 关闭并启动游戏", run_step_0001)
    run_step("step_0002 等待游戏加载到登录界面", run_step_0002)
    run_step("step_0003 点击退出登录按钮", run_step_0003)
    run_step("step_0004 点击协议同意按钮", run_step_0004)
    log_total_time("主流程结束", start_time)


def log_total_time(message: str, start_time: float) -> None:
    log_info(f"{message}，总耗时 {perf_counter() - start_time:.2f} 秒")


if __name__ == "__main__":
    start = perf_counter()
    try:
        main(start)
    except Exception:
        log_total_time("主流程失败", start)
        log_exception("主流程执行失败")
        raise
