from __future__ import annotations

from common.progress_state import advance_after_completed_server
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(10)
    advance_after_completed_server()
