from __future__ import annotations

from collections.abc import Callable

from config import ENABLED_EXTENSIONS
from common.step_runner import run_step
from common.wait_utils import wait_seconds
from extensions.extension_0001_更换种植作物 import run as run_change_crop
from extensions.extension_0002_升级 import run as run_upgrade
from extensions.extension_0003_出售仓库所有东西 import run as run_sell_warehouse
from extensions.extension_0004_开土地 import run as run_open_land
from extensions.extension_0005_一键务农 import run as run_one_click_farm
from extensions.extension_0006_祝福好友 import run as run_bless_friends
from extensions.extension_0007_置顶好友 import run as run_pin_friend


EXTENSION_RUNNERS: dict[str, Callable[[], None]] = {
    "change_crop": run_change_crop,
    "更换种植作物": run_change_crop,
    "sell_warehouse": run_sell_warehouse,
    "出售仓库所有东西": run_sell_warehouse,
    "upgrade": run_upgrade,
    "升级": run_upgrade,
    "open_land": run_open_land,
    "开土地": run_open_land,
    "one_click_farm": run_one_click_farm,
    "一键务农": run_one_click_farm,
    "bless_friends": run_bless_friends,
    "祝福好友": run_bless_friends,
    "pin_friend": run_pin_friend,
    "置顶好友": run_pin_friend,
}


def run_enabled_extensions() -> None:
    for extension_name in ENABLED_EXTENSIONS:
        wait_seconds(1)
        run_extension(extension_name)


def run_extension(extension_name: str) -> None:
    step_func = EXTENSION_RUNNERS.get(extension_name)
    if step_func is None:
        raise ValueError(f"扩展未注册: {extension_name}")
    run_step(f"extension {extension_name}", step_func)
