from __future__ import annotations


def require_point(point: object, label: str) -> tuple[int, int]:
    if not isinstance(point, (list, tuple)) or len(point) != 2:
        raise ValueError(f"{label}坐标必须配置为 [x, y]")
    x, y = point
    return int(x), int(y)
