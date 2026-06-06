from __future__ import annotations

from steps.step_0021_移动到黄色帽子雕塑 import run as move_to_hat_statue
from steps.step_0022_点击一键务农按钮 import run as tap_one_click_farm
from steps.step_0023_随机点击收获页面中间 import run as tap_harvest_continue


def run() -> None:
    move_to_hat_statue()
    tap_one_click_farm()
    tap_harvest_continue()
