from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from config import PROGRESS_STATE_PATH, QQ_ACCOUNT_COUNT, QQ_SELECT_ACCOUNT_FROM_BOTTOM_INDEX, SERVER_SELECT_INDEX
from common.log_utils import log_info


@dataclass
class AutomationProgress:
    account_from_bottom_index: int
    server_index: int
    server_count: int
    finished: bool = False


def create_initial_progress() -> AutomationProgress:
    return AutomationProgress(QQ_SELECT_ACCOUNT_FROM_BOTTOM_INDEX, SERVER_SELECT_INDEX, 0)


def load_progress() -> AutomationProgress:
    if not PROGRESS_STATE_PATH.exists():
        return create_initial_progress()
    return parse_progress(json.loads(PROGRESS_STATE_PATH.read_text(encoding="utf-8")))


def parse_progress(data: dict) -> AutomationProgress:
    default = create_initial_progress()
    return AutomationProgress(
        account_from_bottom_index=int(data.get("account_from_bottom_index", default.account_from_bottom_index)),
        server_index=int(data.get("server_index", default.server_index)),
        server_count=int(data.get("server_count", default.server_count)),
        finished=bool(data.get("finished", default.finished)),
    )


def save_progress(progress: AutomationProgress) -> None:
    PROGRESS_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_STATE_PATH.write_text(json.dumps(asdict(progress), ensure_ascii=False, indent=2), encoding="utf-8")


def reset_progress() -> None:
    save_progress(create_initial_progress())
    log_info("进度已重置到配置起点")


def get_current_account_from_bottom_index() -> int:
    return load_progress().account_from_bottom_index


def get_current_server_index() -> int:
    return load_progress().server_index


def get_current_server_count() -> int:
    return load_progress().server_count


def has_remaining_accounts() -> bool:
    progress = load_progress()
    return not progress.finished and progress.account_from_bottom_index <= QQ_ACCOUNT_COUNT


def save_current_server_count(count: int) -> None:
    progress = load_progress()
    progress.server_count = int(count)
    validate_current_server(progress)
    save_progress(progress)
    log_current_progress(progress)


def validate_current_server(progress: AutomationProgress) -> None:
    if progress.server_count <= 0:
        raise RuntimeError("当前账号识别区服数量为 0")
    if progress.server_index > progress.server_count:
        raise RuntimeError("当前区服索引超过识别区服数量")


def advance_after_completed_server() -> None:
    progress = load_progress()
    advance_progress(progress)
    progress.finished = progress.account_from_bottom_index > QQ_ACCOUNT_COUNT
    save_progress(progress)
    log_current_progress(progress)


def advance_progress(progress: AutomationProgress) -> None:
    if progress.server_index < progress.server_count:
        progress.server_index += 1
        return
    progress.account_from_bottom_index += 1
    progress.server_index = SERVER_SELECT_INDEX
    progress.server_count = 0


def log_current_progress(progress: AutomationProgress) -> None:
    log_info(build_progress_message(progress))


def build_progress_message(progress: AutomationProgress) -> str:
    return f"进度: 账号从下往上第 {progress.account_from_bottom_index} 个，区服 {progress.server_index}/{progress.server_count}"
