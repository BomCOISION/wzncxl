from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from common.template_matcher import read_image_file


def find_template_center(frame: np.ndarray, template_path: Path, threshold: float, region: tuple | None = None) -> tuple[int, int] | None:
    template = load_template_image(template_path)
    match_frame = frame if region is None else crop_region(frame, region)
    result = cv2.matchTemplate(match_frame, template, cv2.TM_CCOEFF_NORMED)
    _, score, _, point = cv2.minMaxLoc(result)
    if score < threshold:
        return None
    return get_template_center(to_screen_point(point, region), template)


def load_template_image(template_path: Path) -> np.ndarray:
    template = read_image_file(template_path)
    if template is None:
        raise FileNotFoundError(f"模板图片不可读: {template_path}")
    return template


def get_template_center(point: tuple[int, int], template: np.ndarray) -> tuple[int, int]:
    x, y = point
    return x + template.shape[1] // 2, y + template.shape[0] // 2


def crop_region(frame: np.ndarray, region: tuple) -> np.ndarray:
    x, y, width, height = get_region_values(region)
    return frame[y:y + height, x:x + width]


def get_region_values(region: tuple) -> tuple[int, int, int, int]:
    if len(region) != 4:
        raise ValueError("模板匹配区域必须配置为 [x, y, 宽, 高]")
    x, y, width, height = region
    return int(x), int(y), int(width), int(height)


def to_screen_point(point: tuple[int, int], region: tuple | None) -> tuple[int, int]:
    if region is None:
        return point
    x, y, _, _ = get_region_values(region)
    return int(point[0] + x), int(point[1] + y)
