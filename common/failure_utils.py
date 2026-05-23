from __future__ import annotations

from pathlib import Path

from config import FAILURE_SCREENSHOT_PATH
from common.run_context import get_context_device
from common.screenshot_utils import save_device_screenshot


def save_failure_screenshot() -> Path:
    target_path = build_failure_screenshot_path()
    return save_device_screenshot(get_context_device(), target_path)


def build_failure_screenshot_path() -> Path:
    FAILURE_SCREENSHOT_PATH.parent.mkdir(exist_ok=True)
    return FAILURE_SCREENSHOT_PATH
