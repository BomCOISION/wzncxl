from __future__ import annotations

from config import HARVEST_PAGE_WAIT_SECONDS, HARVEST_RANDOM_TAP_REGION
from common.random_point_utils import random_point_in_region
from common.run_context import get_context_device
from common.touch_utils import tap_point
from common.wait_utils import wait_seconds


def run() -> None:
    wait_seconds(HARVEST_PAGE_WAIT_SECONDS)
    tap_harvest_page_center(get_context_device())


def tap_harvest_page_center(serial: str) -> None:
    x, y = random_point_in_region(HARVEST_RANDOM_TAP_REGION)
    tap_point(serial, x, y, "收获页面中间随机位置")
