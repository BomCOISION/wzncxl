from __future__ import annotations

from config import FINAL_WAIT_SECONDS
from common.progress_state import advance_after_completed_server
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(FINAL_WAIT_SECONDS)
    advance_after_completed_server()
