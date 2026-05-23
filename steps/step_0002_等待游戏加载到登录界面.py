from __future__ import annotations

from config import (
    GAME_LOAD_TIMEOUT_SECONDS,
    LOGIN_PAGE_REQUIRED_MATCHES,
    LOGIN_PAGE_TEMPLATE_PATHS,
    RETRY_TIMES,
    SCREENSHOT_MEDIAN_FRAME_COUNT,
    TEMPLATE_MATCH_INTERVAL_SECONDS,
    TEMPLATE_MATCH_THRESHOLD,
    TEMPLATE_STABLE_HITS,
)
from common.log_utils import log_info
from common.run_context import get_context_device
from common.template_matcher import MultiTemplateWaitConfig, wait_for_stable_templates


def run() -> None:
    wait_login_page_with_retry(get_context_device())


def wait_login_page_with_retry(serial: str) -> None:
    last_error: Exception | None = None
    for attempt in range(1, RETRY_TIMES + 1):
        last_error = try_wait_login_page(serial, attempt)
        if last_error is None:
            return
    raise RuntimeError(f"[{serial}] 等待游戏加载到登录界面失败") from last_error


def try_wait_login_page(serial: str, attempt: int) -> Exception | None:
    try:
        log_info(f"[{serial}] 等待登录界面，第 {attempt} 次")
        wait_for_stable_templates(serial, "登录界面", create_template_config())
        return None
    except Exception as exc:
        log_info(f"[{serial}] 登录界面未稳定出现: {exc}")
        return exc


def create_template_config() -> MultiTemplateWaitConfig:
    return MultiTemplateWaitConfig(
        template_paths=LOGIN_PAGE_TEMPLATE_PATHS,
        required_matches=LOGIN_PAGE_REQUIRED_MATCHES,
        timeout_seconds=GAME_LOAD_TIMEOUT_SECONDS,
        frame_count=SCREENSHOT_MEDIAN_FRAME_COUNT,
        threshold=TEMPLATE_MATCH_THRESHOLD,
        stable_hits=TEMPLATE_STABLE_HITS,
        interval_seconds=TEMPLATE_MATCH_INTERVAL_SECONDS,
    )
