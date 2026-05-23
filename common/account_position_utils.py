from __future__ import annotations


def calculate_account_point(first_point: tuple, row_height: int, account_index: int) -> tuple[int, int]:
    """计算指定账号序号的点击坐标"""
    x, first_y = first_point
    return int(x), int(first_y) + (account_index - 1) * row_height


def calculate_index_from_bottom(account_count: int, bottom_index: int) -> int:
    """把从下往上序号换算成从上往下序号"""
    validate_account_index(account_count, bottom_index)
    return account_count - bottom_index + 1


def validate_account_index(account_count: int, bottom_index: int) -> None:
    """检查账号数量和选择序号"""
    if account_count <= 0:
        raise ValueError("QQ 账号数量必须大于 0")
    if bottom_index < 1 or bottom_index > account_count:
        raise ValueError("从下往上选择序号超出账号数量")
