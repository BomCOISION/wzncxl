from __future__ import annotations

from config import AGREEMENT_AGREE_BUTTON_POINT
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(1)
    tap_agreement_agree_button(get_context_device())


def tap_agreement_agree_button(serial: str) -> None:
    x, y = AGREEMENT_AGREE_BUTTON_POINT
    tap_point(serial, int(x), int(y), "协议同意按钮")
