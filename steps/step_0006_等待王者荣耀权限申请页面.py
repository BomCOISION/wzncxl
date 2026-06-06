from __future__ import annotations

from config import (
    PERMISSION_PAGE_LIVE_SCREENSHOT_PATH,
    PERMISSION_PAGE_TEMPLATE_PATHS,
    RETRY_TIMES,
)
from common.log_utils import log_info
from common.run_context import get_context_device
from common.screenshot_utils import save_device_screenshot
from common.template_matcher import MultiTemplateWaitConfig, wait_for_stable_templates


def run() -> None:
    wait_permission_page_with_retry(get_context_device())


def wait_permission_page_with_retry(serial: str) -> None:
    last_error: Exception | None = None
    for attempt in range(1, RETRY_TIMES + 1):
        last_error = try_wait_permission_page(serial, attempt)
        if last_error is None:
            return
    raise RuntimeError(f"[{serial}] 等待王者荣耀权限申请页面失败") from last_error


def try_wait_permission_page(serial: str, attempt: int) -> Exception | None:
    try:
        save_permission_live_screen(serial)
        wait_for_permission_page(serial, attempt)
        return None
    except Exception as exc:
        log_info(f"[{serial}] 权限申请页面未稳定出现: {exc}")
        return exc


def save_permission_live_screen(serial: str) -> None:
    path = save_device_screenshot(serial, PERMISSION_PAGE_LIVE_SCREENSHOT_PATH)
    log_info(f"[{serial}] 已保存权限页实时截图: {path}")


def wait_for_permission_page(serial: str, attempt: int) -> None:
    log_info(f"[{serial}] 等待权限申请页面，第 {attempt} 次")
    wait_for_stable_templates(serial, "王者荣耀权限申请页面", create_template_config())


def create_template_config() -> MultiTemplateWaitConfig:
    return MultiTemplateWaitConfig(
        template_paths=PERMISSION_PAGE_TEMPLATE_PATHS,
        required_matches=2,
        timeout_seconds=15,
        frame_count=5,
        threshold=0.82,
        stable_hits=1,
        interval_seconds=0.8,
    )
