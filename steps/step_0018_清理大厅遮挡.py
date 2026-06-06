from __future__ import annotations

from config import LOBBY_CLEAR_MAX_ROUNDS
from common.log_utils import log_info
from common.run_context import get_context_device
from common.wait_utils import wait_seconds
from steps.step_0015_识别并关闭弹窗 import close_popup
from steps.step_0016_判断干净大厅 import is_clean_lobby_once
from steps.step_0017_识别并返回活动页 import back_activity


def run() -> None:
    clear_lobby_blockers(get_context_device())


def clear_lobby_blockers(serial: str) -> None:
    stable_hits = 0
    for round_index in range(1, LOBBY_CLEAR_MAX_ROUNDS + 1):
        stable_hits = handle_lobby_round(serial, round_index, stable_hits)
        if stable_hits >= 2:
            return
    raise RuntimeError(f"[{serial}] 清理大厅遮挡后仍未进入干净大厅")


def handle_lobby_round(serial: str, round_index: int, stable_hits: int) -> int:
    stable_hits = update_clean_lobby_hits(serial, round_index, stable_hits)
    if stable_hits:
        wait_seconds(2)
        return stable_hits
    clear_one_blocker(serial)
    wait_seconds(2)
    return 0


def update_clean_lobby_hits(serial: str, round_index: int, stable_hits: int) -> int:
    if is_clean_lobby_once(serial):
        return log_clean_lobby_hit(serial, stable_hits + 1)
    log_info(f"[{serial}] 第 {round_index} 轮未识别为干净大厅")
    return 0


def log_clean_lobby_hit(serial: str, stable_hits: int) -> int:
    log_info(f"[{serial}] 干净大厅稳定命中 {stable_hits}/2")
    return stable_hits


def clear_one_blocker(serial: str) -> None:
    if close_popup(serial):
        return
    if back_activity(serial):
        return
    log_info(f"[{serial}] 未识别到可清理遮挡")
