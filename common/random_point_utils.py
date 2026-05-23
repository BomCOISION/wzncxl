from __future__ import annotations

from random import randint


def random_point_in_region(region: tuple) -> tuple[int, int]:
    x, y, width, height = [int(value) for value in region]
    return randint(x, x + width), randint(y, y + height)
