from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from time import monotonic, sleep

import cv2
import numpy as np

from config import ADB_PATH
from common.adb_client import ADBClient
from common.log_utils import log_info


@dataclass
class MultiTemplateWaitConfig:
    template_paths: list[Path]
    required_matches: int
    timeout_seconds: float
    frame_count: int
    threshold: float
    stable_hits: int
    interval_seconds: float


@dataclass
class TemplateMatchResult:
    scores: dict[str, float]
    pass_count: int


@dataclass
class MultiTemplateWaitState:
    deadline: float
    hit_count: int = 0
    best_pass_count: int = 0
    best_scores: dict[str, float] = field(default_factory=dict)


def wait_for_stable_templates(serial: str, page_name: str, config: MultiTemplateWaitConfig) -> None:
    templates = load_templates(config.template_paths)
    client = create_adb_client(serial)
    state = create_multi_wait_state(config.timeout_seconds)
    while monotonic() < state.deadline:
        if detect_templates_once(client, page_name, templates, config, state):
            return
    raise_multi_timeout_error(serial, page_name, state)


def detect_templates_once(client: ADBClient, page_name: str, templates: dict[str, np.ndarray], config: MultiTemplateWaitConfig, state: MultiTemplateWaitState) -> bool:
    result = get_template_result(client, templates, config)
    update_multi_state(state, result, config.required_matches)
    if state.hit_count >= config.stable_hits:
        log_multi_match_success(client.device_serial, page_name, result)
        return True
    sleep(config.interval_seconds)
    return False


def get_template_result(client: ADBClient, templates: dict[str, np.ndarray], config: MultiTemplateWaitConfig) -> TemplateMatchResult:
    scores = score_templates(client.median_frame(config.frame_count), templates)
    return TemplateMatchResult(scores=scores, pass_count=count_passed(scores, config.threshold))


def score_templates(frame: np.ndarray, templates: dict[str, np.ndarray]) -> dict[str, float]:
    return {name: match_template(frame, template) for name, template in templates.items()}


def count_passed(scores: dict[str, float], threshold: float) -> int:
    return sum(score >= threshold for score in scores.values())


def match_template(frame: np.ndarray, template: np.ndarray) -> float:
    check_template_size(frame, template)
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    return float(cv2.minMaxLoc(result)[1])


def load_templates(template_paths: list[Path]) -> dict[str, np.ndarray]:
    templates = {path.stem: load_template(path) for path in template_paths}
    if not templates:
        raise ValueError("模板列表不能为空")
    return templates


def load_template(template_path: Path) -> np.ndarray:
    template = read_image_file(template_path)
    if template is None:
        raise FileNotFoundError(f"模板图片不存在或不可读: {template_path}")
    return template


def read_image_file(image_path: Path) -> np.ndarray | None:
    if not image_path.exists():
        return None
    data = np.fromfile(str(image_path), dtype=np.uint8)
    if data.size == 0:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def create_adb_client(serial: str) -> ADBClient:
    return ADBClient(str(ADB_PATH), serial)


def create_multi_wait_state(timeout_seconds: float) -> MultiTemplateWaitState:
    return MultiTemplateWaitState(deadline=monotonic() + timeout_seconds)


def update_multi_state(state: MultiTemplateWaitState, result: TemplateMatchResult, required_matches: int) -> None:
    state.best_pass_count = max(state.best_pass_count, result.pass_count)
    state.best_scores = merge_best_scores(state.best_scores, result.scores)
    state.hit_count = update_hit_count(result.pass_count, required_matches, state.hit_count)


def merge_best_scores(old_scores: dict[str, float], new_scores: dict[str, float]) -> dict[str, float]:
    best_scores = dict(old_scores)
    for name, score in new_scores.items():
        best_scores[name] = max(best_scores.get(name, 0.0), score)
    return best_scores


def update_hit_count(pass_count: int, required_matches: int, hit_count: int) -> int:
    return hit_count + 1 if pass_count >= required_matches else 0


def check_template_size(frame: np.ndarray, template: np.ndarray) -> None:
    if frame.shape[0] < template.shape[0] or frame.shape[1] < template.shape[1]:
        raise ValueError("模板尺寸不能大于截图尺寸")


def log_multi_match_success(serial: str, page_name: str, result: TemplateMatchResult) -> None:
    log_info(f"[{serial}] {page_name} 已稳定命中，{result.pass_count} 个模板达标，分数: {format_scores(result.scores)}")


def format_scores(scores: dict[str, float]) -> str:
    return ", ".join(f"{name}={score:.3f}" for name, score in scores.items())


def raise_multi_timeout_error(serial: str, page_name: str, state: MultiTemplateWaitState) -> None:
    scores = format_scores(state.best_scores)
    raise TimeoutError(f"[{serial}] 等待{page_name}超时，最多 {state.best_pass_count} 个模板达标，最高分数: {scores}")
