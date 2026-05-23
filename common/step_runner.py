from __future__ import annotations

from collections.abc import Callable
from time import perf_counter

from common.log_utils import log_error, log_info


def run_step(step_name: str, step_func: Callable[[], None]) -> None:
    """执行步骤并记录耗时"""
    start_time = perf_counter()
    log_info(f"{step_name} 开始")
    try:
        step_func()
    except Exception:
        log_step_failed(step_name, start_time)
        raise
    log_step_finished(step_name, start_time)


def log_step_failed(step_name: str, start_time: float) -> None:
    """记录步骤失败耗时"""
    log_error(f"{step_name} 失败，耗时 {format_elapsed_seconds(start_time)} 秒")


def log_step_finished(step_name: str, start_time: float) -> None:
    """记录步骤结束耗时"""
    log_info(f"{step_name} 结束，耗时 {format_elapsed_seconds(start_time)} 秒")


def format_elapsed_seconds(start_time: float) -> str:
    """格式化步骤耗时"""
    return f"{perf_counter() - start_time:.2f}"
