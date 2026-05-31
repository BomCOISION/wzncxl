from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from config import (
    CROP_LIST_MATCH_DEDUP_X,
    CROP_LIST_MATCH_DEDUP_Y,
    CROP_LIST_MATCH_REGION,
    CROP_LIST_MATCH_RESULT_IMAGE_PATH,
    CROP_LIST_MATCH_THRESHOLD,
    CROP_LIST_TARGET_CROP_TIME,
    CROP_LIST_TIME_TEMPLATE_PATHS,
    CROP_LIST_TIME_TO_ICON_OFFSET,
    CROP_ICON_MATCH_DEDUP_X,
    CROP_ICON_MATCH_DEDUP_Y,
    CROP_ICON_MATCH_THRESHOLD,
    CROP_ICON_PRIORITY_GROUPS,
    CROP_ICON_TEMPLATE_PATHS,
)


def scan_crop_list(image_path: Path) -> dict[str, Any]:
    image = read_image(image_path)
    items = scan_all_templates(image)
    crop_items = scan_all_crop_icons(image)
    save_result_image(image, items + crop_items)
    return create_scan_result(items, crop_items)


def create_scan_result(items: list[dict[str, Any]], crop_items: list[dict[str, Any]]) -> dict[str, Any]:
    target = find_right_bottom_crop_icon(items, CROP_LIST_TARGET_CROP_TIME)
    return create_result_data(items, crop_items, target)


def create_result_data(items: list[dict[str, Any]], crop_items: list[dict[str, Any]], target: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "total": len(items),
        "target_crop_icon": target,
        "priority_crop_icons": create_priority_icons(crop_items),
        "by_time": group_items_by_time(items),
        "items": items,
        "crop_items": crop_items,
    }


def read_image(image_path: Path) -> np.ndarray:
    data = np.fromfile(str(image_path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"作物列表截图不可读: {image_path}")
    return image


def scan_all_templates(image: np.ndarray) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for time_name, template_path in CROP_LIST_TIME_TEMPLATE_PATHS.items():
        items.extend(match_time_template(image, time_name, template_path))
    return sorted(items, key=lambda item: (item["point"][1], item["point"][0]))


def scan_all_crop_icons(image: np.ndarray) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for crop_name, template_path in CROP_ICON_TEMPLATE_PATHS.items():
        items.extend(match_crop_icon_template(image, crop_name, template_path))
    return sorted(items, key=lambda item: (item["point"][1], item["point"][0]))


def match_crop_icon_template(image: np.ndarray, crop_name: str, template_path: Path) -> list[dict[str, Any]]:
    template = try_read_template(template_path)
    if template is None:
        return []
    region_image = crop_match_region(image)
    points = match_crop_icon_points(region_image, template)
    return [create_crop_icon_item(crop_name, point, template) for point in points]


def match_crop_icon_points(image: np.ndarray, template: np.ndarray) -> list[tuple[int, int]]:
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    rows, cols = np.where(result >= CROP_ICON_MATCH_THRESHOLD)
    return dedup_crop_icon_points(to_screen_points(cols, rows, template))


def dedup_crop_icon_points(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    unique: list[tuple[int, int]] = []
    for point in points:
        append_unique_crop_icon_point(unique, point)
    return unique


def append_unique_crop_icon_point(unique: list[tuple[int, int]], point: tuple[int, int]) -> None:
    if all(is_distinct_crop_icon_point(point, old_point) for old_point in unique):
        unique.append(point)


def is_distinct_crop_icon_point(point: tuple[int, int], old_point: tuple[int, int]) -> bool:
    return abs(point[0] - old_point[0]) > CROP_ICON_MATCH_DEDUP_X or abs(point[1] - old_point[1]) > CROP_ICON_MATCH_DEDUP_Y


def match_time_template(image: np.ndarray, time_name: str, template_path: Path) -> list[dict[str, Any]]:
    template = read_template(template_path)
    region_image = crop_match_region(image)
    points = match_template_points(region_image, template)
    return [create_item(time_name, point, template) for point in points]


def read_template(template_path: Path) -> np.ndarray:
    template = read_image(template_path)
    if template is None:
        raise FileNotFoundError(f"作物时间模板不可读: {template_path}")
    return template


def try_read_template(template_path: Path) -> np.ndarray | None:
    if not template_path.exists():
        return None
    return read_image(template_path)


def crop_match_region(image: np.ndarray) -> np.ndarray:
    x, y, width, height = get_match_region()
    return image[y:y + height, x:x + width]


def get_match_region() -> tuple[int, int, int, int]:
    if len(CROP_LIST_MATCH_REGION) != 4:
        raise ValueError("crop_list_match_region 必须配置为 [x, y, 宽, 高]")
    x, y, width, height = CROP_LIST_MATCH_REGION
    return int(x), int(y), int(width), int(height)


def match_template_points(image: np.ndarray, template: np.ndarray) -> list[tuple[int, int]]:
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    rows, cols = np.where(result >= CROP_LIST_MATCH_THRESHOLD)
    return dedup_points(to_screen_points(cols, rows, template))


def to_screen_points(cols, rows, template: np.ndarray) -> list[tuple[int, int]]:
    x, y, _, _ = get_match_region()
    h, w = template.shape[:2]
    return [(int(col) + w // 2 + x, int(row) + h // 2 + y) for row, col in zip(rows, cols)]


def dedup_points(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    unique: list[tuple[int, int]] = []
    for point in points:
        append_unique_point(unique, point)
    return unique


def append_unique_point(unique: list[tuple[int, int]], point: tuple[int, int]) -> None:
    if all(is_distinct_point(point, old_point) for old_point in unique):
        unique.append(point)


def is_distinct_point(point: tuple[int, int], old_point: tuple[int, int]) -> bool:
    return abs(point[0] - old_point[0]) > CROP_LIST_MATCH_DEDUP_X or abs(point[1] - old_point[1]) > CROP_LIST_MATCH_DEDUP_Y


def create_item(time_name: str, point: tuple[int, int], template: np.ndarray) -> dict[str, Any]:
    h, w = template.shape[:2]
    return {"time": time_name, "point": list(point), "icon_point": get_icon_point(point), "box": create_box(point, w, h)}


def create_crop_icon_item(crop_name: str, point: tuple[int, int], template: np.ndarray) -> dict[str, Any]:
    h, w = template.shape[:2]
    return {"crop": crop_name, "point": list(point), "icon_point": list(point), "box": create_box(point, w, h)}


def get_icon_point(time_point: tuple[int, int]) -> list[int]:
    offset_x, offset_y = CROP_LIST_TIME_TO_ICON_OFFSET
    return [int(time_point[0] + offset_x), int(time_point[1] + offset_y)]


def create_box(point: tuple[int, int], width: int, height: int) -> list[int]:
    x, y = point
    return [x - width // 2, y - height // 2, x + width // 2, y + height // 2]


def save_result_image(image: np.ndarray, items: list[dict[str, Any]]) -> None:
    result_image = image.copy()
    for item in items:
        draw_item_box(result_image, item)
    write_image(CROP_LIST_MATCH_RESULT_IMAGE_PATH, result_image)


def draw_item_box(image: np.ndarray, item: dict[str, Any]) -> None:
    x1, y1, x2, y2 = item["box"]
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)


def write_image(path: Path, image: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError("作物识别结果图编码失败")
    encoded.tofile(str(path))


def group_items_by_time(items: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        groups.setdefault(item["time"], []).append(item)
    return {time: {"count": len(values), "items": values} for time, values in groups.items()}


def find_right_bottom_crop_icon(items: list[dict[str, Any]], time_name: str) -> dict[str, Any] | None:
    candidates = [item for item in items if item["time"] == time_name]
    if not candidates:
        return None
    item = max(candidates, key=get_right_bottom_score)
    return {"time": time_name, "point": item["icon_point"], "time_point": item["point"]}


def create_priority_icons(crop_items: list[dict[str, Any]]) -> dict[str, Any]:
    return {str(flag): find_priority_crop_icon(crop_items, flag) for flag in CROP_ICON_PRIORITY_GROUPS}


def find_priority_crop_icon(crop_items: list[dict[str, Any]], flag: int) -> dict[str, Any] | None:
    for crop_name in get_priority_crop_names(flag):
        target = find_right_bottom_crop_name(crop_items, crop_name)
        if target is not None:
            return target
    return find_fallback_priority_crop_icon(crop_items, flag)


def get_priority_crop_names(flag: int) -> list[str]:
    return CROP_ICON_PRIORITY_GROUPS.get(flag, [])


def find_right_bottom_crop_name(crop_items: list[dict[str, Any]], crop_name: str) -> dict[str, Any] | None:
    candidates = [item for item in crop_items if item["crop"] == crop_name]
    if not candidates:
        return None
    item = max(candidates, key=get_right_bottom_score)
    return {"flag": get_crop_flag(crop_name), "crop": crop_name, "point": item["point"]}


def get_crop_flag(crop_name: str) -> int:
    for flag, names in CROP_ICON_PRIORITY_GROUPS.items():
        if crop_name in names:
            return flag
    return 3


def find_fallback_priority_crop_icon(crop_items: list[dict[str, Any]], flag: int) -> dict[str, Any] | None:
    if flag != 1:
        return None
    for next_flag in get_later_priority_flags(flag):
        target = find_priority_crop_icon(crop_items, next_flag)
        if target is not None:
            return target
    return None


def get_later_priority_flags(flag: int) -> list[int]:
    return sorted(next_flag for next_flag in CROP_ICON_PRIORITY_GROUPS if next_flag > flag)


def get_right_bottom_score(item: dict[str, Any]) -> tuple[int, int]:
    x, y = item["point"]
    return y, x


def save_crop_scan_result(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def format_crop_scan_result(result: dict[str, Any]) -> str:
    lines = [f"模板匹配到目标作物时间数量: {result['total']}"]
    lines.append(format_target_crop_icon(result.get("target_crop_icon")))
    lines.extend(format_time_group(time, group) for time, group in result["by_time"].items())
    return "\n".join(lines)


def format_target_crop_icon(target: dict[str, Any] | None) -> str:
    if target is None:
        return "最靠右下目标作物图标: 未找到"
    x, y = target["point"]
    return f"最靠右下{target['time']}作物图标: ({x}, {y})"


def format_time_group(time: str, group: dict[str, Any]) -> str:
    items = "，".join(format_group_item(item) for item in group["items"])
    return f"{time}: {group['count']} 个，{items}"


def format_group_item(item: dict[str, Any]) -> str:
    x, y = item["point"]
    return f"({x}, {y})"
