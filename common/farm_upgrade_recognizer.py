from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from config import (
    FARM_UPGRADE_ARROW_MATCH_REGION,
    FARM_UPGRADE_ARROW_TEMPLATE_PATH,
)


def scan_farm_upgrade(image_path: Path) -> dict[str, Any]:
    image = read_image(image_path)
    template = read_image(FARM_UPGRADE_ARROW_TEMPLATE_PATH)
    score, point, box = match_upgrade_arrow(image, template)
    return create_scan_result(score, point, box)


def match_upgrade_arrow(image: np.ndarray, template: np.ndarray) -> tuple[float, list[int], list[int]]:
    region = crop_upgrade_region(image)
    result = cv2.matchTemplate(region, template, cv2.TM_CCOEFF_NORMED)
    _, score, _, location = cv2.minMaxLoc(result)
    point = create_screen_point(location, template)
    return float(score), point, create_box(point, template)


def crop_upgrade_region(image: np.ndarray) -> np.ndarray:
    x, y, width, height = get_upgrade_region()
    return image[y:y + height, x:x + width]


def get_upgrade_region() -> tuple[int, int, int, int]:
    if len(FARM_UPGRADE_ARROW_MATCH_REGION) != 4:
        raise ValueError("farm_upgrade_arrow_match_region 必须配置为 [x, y, 宽, 高]")
    x, y, width, height = FARM_UPGRADE_ARROW_MATCH_REGION
    return int(x), int(y), int(width), int(height)


def create_screen_point(location: tuple[int, int], template: np.ndarray) -> list[int]:
    x, y, _, _ = get_upgrade_region()
    h, w = template.shape[:2]
    return [int(location[0] + x + w // 2), int(location[1] + y + h // 2)]


def create_box(point: list[int], template: np.ndarray) -> list[int]:
    h, w = template.shape[:2]
    x, y = point
    return [x - w // 2, y - h // 2, x + w // 2, y + h // 2]


def create_scan_result(score: float, point: list[int], box: list[int]) -> dict[str, Any]:
    can_upgrade = score >= 0.9
    return {
        "can_upgrade": can_upgrade,
        "score": round(score, 4),
        "threshold": 0.9,
        "point": point if can_upgrade else None,
        "box": box if can_upgrade else None,
    }


def read_image(image_path: Path) -> np.ndarray:
    data = np.fromfile(str(image_path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"升级判断图片不可读: {image_path}")
    return image


def save_upgrade_result(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
