from __future__ import annotations

from config import (
    LOBBY_CLEAN_TEMPLATE_REGIONS,
    LOBBY_CLEAN_TEMPLATE_PATHS,
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
        required_matches=4,
        timeout_seconds=20,
        frame_count=5,
        threshold=0.82,
        stable_hits=2,
        interval_seconds=0.8,
        template_regions=LOBBY_CLEAN_TEMPLATE_REGIONS,
    )
