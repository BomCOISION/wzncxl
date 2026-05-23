from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from common.template_matcher import read_image_file


def count_server_status_icons(frame: np.ndarray, template_paths: list[Path], region: tuple, threshold: float, distance: int) -> int:
    return len(find_sorted_server_status_points(frame, template_paths, region, threshold, distance))


def find_sorted_server_status_points(frame: np.ndarray, template_paths: list[Path], region: tuple, threshold: float, distance: int) -> list[tuple[int, int]]:
    points = find_status_icon_points(crop_region(frame, region), template_paths, threshold, region)
    return sort_points_by_row(deduplicate_points(points, distance))


def crop_region(frame: np.ndarray, region: tuple) -> np.ndarray:
    x, y, width, height = [int(value) for value in region]
    return frame[y:y + height, x:x + width]


def find_status_icon_points(frame: np.ndarray, template_paths: list[Path], threshold: float, region: tuple) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for template_path in template_paths:
        points.extend(match_template_points(frame, load_status_template(template_path), threshold, region))
    return points


def load_status_template(template_path: Path) -> np.ndarray:
    template = read_image_file(template_path)
    if template is None:
        raise FileNotFoundError(f"状态图标模板不可读: {template_path}")
    return template


def match_template_points(frame: np.ndarray, template: np.ndarray, threshold: float, region: tuple) -> list[tuple[int, int]]:
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    rows, cols = np.where(result >= threshold)
    return [to_screen_point(col, row, template, region) for row, col in zip(rows, cols)]


def to_screen_point(col: int, row: int, template: np.ndarray, region: tuple) -> tuple[int, int]:
    x, y, _, _ = [int(value) for value in region]
    return x + col + template.shape[1] // 2, y + row + template.shape[0] // 2


def deduplicate_points(points: list[tuple[int, int]], distance: int) -> list[tuple[int, int]]:
    unique: list[tuple[int, int]] = []
    for point in sorted(points, key=lambda item: (item[1], item[0])):
        append_unique_point(unique, point, distance)
    return unique


def sort_points_by_row(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted(points, key=lambda item: (item[1], item[0]))


def append_unique_point(points: list[tuple[int, int]], point: tuple[int, int], distance: int) -> None:
    if all(point_distance(point, old_point) > distance for old_point in points):
        points.append(point)


def point_distance(first: tuple[int, int], second: tuple[int, int]) -> float:
    return float(np.hypot(first[0] - second[0], first[1] - second[1]))
