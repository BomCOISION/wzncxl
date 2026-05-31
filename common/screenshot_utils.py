from __future__ import annotations

from pathlib import Path

import cv2

from config import ADB_PATH, SCREENSHOT_MEDIAN_FRAME_COUNT
from common.adb_client import ADBClient


def save_device_screenshot(serial: str, target_path: Path) -> Path:
    """保存设备当前实时截图"""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    image = ADBClient(str(ADB_PATH), serial).screenshot()
    if image is None:
        raise RuntimeError("设备截图为空")
    write_image(target_path, image)
    return target_path


def save_device_median_screenshot(serial: str, target_path: Path) -> Path:
    """保存设备连续截图中位图"""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    image = ADBClient(str(ADB_PATH), serial).median_frame(SCREENSHOT_MEDIAN_FRAME_COUNT)
    write_image(target_path, image)
    return target_path


def write_image(path: Path, image) -> None:
    """写入 PNG 图片"""
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError("截图编码失败")
    encoded.tofile(str(path))
