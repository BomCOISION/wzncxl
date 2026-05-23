from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from common.template_matcher import read_image_file


def find_template_center(frame: np.ndarray, template_path: Path, threshold: float) -> tuple[int, int] | None:
    template = load_template_image(template_path)
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    _, score, _, point = cv2.minMaxLoc(result)
    if score < threshold:
        return None
    return get_template_center(point, template)


def load_template_image(template_path: Path) -> np.ndarray:
    template = read_image_file(template_path)
    if template is None:
        raise FileNotFoundError(f"模板图片不可读: {template_path}")
    return template


def get_template_center(point: tuple[int, int], template: np.ndarray) -> tuple[int, int]:
    x, y = point
    return x + template.shape[1] // 2, y + template.shape[0] // 2
