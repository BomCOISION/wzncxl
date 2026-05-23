from __future__ import annotations

from config import TARGET_DEVICES


def get_context_device() -> str:
    if not TARGET_DEVICES:
        raise ValueError("TARGET_DEVICES 不能为空")
    return TARGET_DEVICES[0]


def get_context_devices() -> list[str]:
    """获取当前执行设备列表"""
    return list(TARGET_DEVICES)
