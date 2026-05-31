from __future__ import annotations

from config import (
    FARM_LOADED_REQUIRED_MATCHES,
    FARM_LOADED_STABLE_HITS,
    FARM_LOADED_TEMPLATE_REGIONS,
    FARM_LOADED_TEMPLATE_PATHS,
    FARM_LOADED_TIMEOUT_SECONDS,
    SCREENSHOT_MEDIAN_FRAME_COUNT,
    TEMPLATE_MATCH_INTERVAL_SECONDS,
    TEMPLATE_MATCH_THRESHOLD,
)
from common.run_context import get_context_device
from common.template_matcher import MultiTemplateWaitConfig, wait_for_stable_templates


def run() -> None:
    wait_farm_loaded(get_context_device())


def wait_farm_loaded(serial: str) -> None:
    wait_for_stable_templates(serial, "农场加载完成", create_template_config())


def create_template_config() -> MultiTemplateWaitConfig:
    return MultiTemplateWaitConfig(
        template_paths=FARM_LOADED_TEMPLATE_PATHS,
        required_matches=FARM_LOADED_REQUIRED_MATCHES,
        timeout_seconds=FARM_LOADED_TIMEOUT_SECONDS,
        frame_count=SCREENSHOT_MEDIAN_FRAME_COUNT,
        threshold=TEMPLATE_MATCH_THRESHOLD,
        stable_hits=FARM_LOADED_STABLE_HITS,
        interval_seconds=TEMPLATE_MATCH_INTERVAL_SECONDS,
        template_regions=FARM_LOADED_TEMPLATE_REGIONS,
    )
