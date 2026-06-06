from __future__ import annotations

from time import monotonic

from config import (
    ADB_PATH,
    FARM_LOADED_ACTIVITY_BACK_BUTTON_POINT,
    FARM_LOADED_BACK_POPUP_CLOSE_POINT,
    FARM_LOADED_TEMPLATE_REGIONS,
    FARM_LOADED_TEMPLATE_PATHS,
)
from common.adb_client import ADBClient
from common.run_context import get_context_device
from common.template_matcher import (
    MultiTemplateWaitConfig,
    MultiTemplateWaitState,
    create_multi_wait_state,
    load_templates,
    log_multi_match_round,
    log_multi_match_success,
    raise_multi_timeout_error,
    try_get_template_result,
    update_multi_state,
)
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_farm_loaded(get_context_device())


def wait_farm_loaded(serial: str) -> None:
    config = create_template_config()
    templates = load_templates(config.template_paths)
    client = ADBClient(str(ADB_PATH), serial)
    state = create_multi_wait_state(config.timeout_seconds)
    wait_until_farm_loaded(client, templates, config, state)
    wait_seconds(config.interval_seconds)
    close_back_popup_if_opened(client.device_serial)


def wait_until_farm_loaded(client: ADBClient, templates: dict, config: MultiTemplateWaitConfig, state) -> None:
    while monotonic() < state.deadline:
        if detect_farm_loaded_once(client, templates, config, state):
            return
        close_back_popup_if_opened(client.device_serial)
        wait_seconds(config.interval_seconds)
    raise_multi_timeout_error(client.device_serial, "农场加载完成", state)


def detect_farm_loaded_once(client: ADBClient, templates: dict, config: MultiTemplateWaitConfig, state: MultiTemplateWaitState) -> bool:
    state.round_index += 1
    result = try_get_template_result(client, "农场加载完成", templates, config, state)
    if result is None:
        return False
    update_multi_state(state, result, config.required_matches)
    log_multi_match_round(client.device_serial, "农场加载完成", state, result, config)
    return log_success_if_stable(client, config, state, result)


def log_success_if_stable(client: ADBClient, config: MultiTemplateWaitConfig, state: MultiTemplateWaitState, result) -> bool:
    if state.hit_count < config.stable_hits:
        return False
    log_multi_match_success(client.device_serial, "农场加载完成", result)
    return True


def create_template_config() -> MultiTemplateWaitConfig:
    return MultiTemplateWaitConfig(
        template_paths=FARM_LOADED_TEMPLATE_PATHS,
        required_matches=3,
        timeout_seconds=60,
        frame_count=5,
        threshold=0.82,
        stable_hits=1,
        interval_seconds=0.8,
        template_regions=FARM_LOADED_TEMPLATE_REGIONS,
    )


def tap_activity_back_button(serial: str) -> None:
    tap_point(serial, int(598), int(706), "活动页返回按钮")
    tap_point(serial, int(598), int(706), "活动页返回按钮")
    x, y = FARM_LOADED_ACTIVITY_BACK_BUTTON_POINT
    tap_point(serial, int(x), int(y), "活动页返回按钮")
    wait_seconds(0.2)
    tap_point(serial, int(x), int(y), "活动页返回按钮")
    wait_seconds(1)
    tap_point(serial, int(598), int(706), "活动页返回按钮")



def close_back_popup_if_opened(serial: str) -> None:
    tap_activity_back_button(serial)
    wait_seconds(0.2)
    tap_back_popup_close_button(serial)


def tap_back_popup_close_button(serial: str) -> None:
    x, y = FARM_LOADED_BACK_POPUP_CLOSE_POINT
    tap_point(serial, int(x), int(y), "农场返回弹窗关闭按钮")
