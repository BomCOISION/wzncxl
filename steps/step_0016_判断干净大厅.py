from __future__ import annotations

from config import (
    LOBBY_CLEAN_REQUIRED_MATCHES,
    LOBBY_CLEAN_STABLE_HITS,
    LOBBY_CLEAN_TEMPLATE_REGIONS,
    LOBBY_CLEAN_TEMPLATE_PATHS,
    LOBBY_CLEAN_TIMEOUT_SECONDS,
    SCREENSHOT_MEDIAN_FRAME_COUNT,
    TEMPLATE_MATCH_INTERVAL_SECONDS,
    TEMPLATE_MATCH_THRESHOLD,
)
from common.run_context import get_context_device
from common.template_matcher import MultiTemplateWaitConfig, detect_templates_once_only, wait_for_stable_templates


def run() -> None:
    wait_clean_lobby(get_context_device())


def wait_clean_lobby(serial: str) -> None:
    wait_for_stable_templates(serial, "干净大厅", create_template_config())


def is_clean_lobby_once(serial: str) -> bool:
    return detect_templates_once_only(serial, "干净大厅", create_template_config())


def create_template_config() -> MultiTemplateWaitConfig:
    return MultiTemplateWaitConfig(
        template_paths=LOBBY_CLEAN_TEMPLATE_PATHS,
        required_matches=LOBBY_CLEAN_REQUIRED_MATCHES,
        timeout_seconds=LOBBY_CLEAN_TIMEOUT_SECONDS,
        frame_count=SCREENSHOT_MEDIAN_FRAME_COUNT,
        threshold=TEMPLATE_MATCH_THRESHOLD,
        stable_hits=LOBBY_CLEAN_STABLE_HITS,
        interval_seconds=TEMPLATE_MATCH_INTERVAL_SECONDS,
        template_regions=LOBBY_CLEAN_TEMPLATE_REGIONS,
    )
