from __future__ import annotations

from common.logger import 获取日志器


def log_info(message: str) -> None:
    """记录普通日志"""
    获取日志器().info(message)


def log_error(message: str) -> None:
    """记录错误日志"""
    获取日志器().error(message)


def log_exception(message: str) -> None:
    """记录异常日志"""
    获取日志器().exception(message)
