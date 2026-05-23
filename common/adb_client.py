from dataclasses import dataclass
from pathlib import Path
import subprocess
import cv2
import numpy as np

from config import ADB_COMMAND_TIMEOUT_SECONDS


class ADBError(RuntimeError):
    pass


@dataclass
class ADBClient:
    adb_path: str
    device_serial: str

    def __post_init__(self) -> None:
        self.adb_path = self.adb_path.strip()

    def base(self) -> list[str]:
        return [self.adb_path, "-s", self.device_serial]

    def ensure_adb_exists(self) -> None:
        if self.adb_path == "adb" or Path(self.adb_path).is_file():
            return
        raise ADBError(f"adb executable not found: {self.adb_path}")

    def run(self, args: list[str]) -> str:
        self.ensure_adb_exists()
        result = run_adb_process(self.base() + args, text=True)
        if result.returncode:
            raise ADBError(result.stderr.strip() or "adb command failed")
        return result.stdout.strip()

    def run_bytes(self, args: list[str]) -> bytes:
        self.ensure_adb_exists()
        result = run_adb_process(self.base() + args)
        if result.returncode:
            raise ADBError(result.stderr.decode(errors="ignore").strip())
        return result.stdout

    def list_devices(self) -> list[str]:
        self.ensure_adb_exists()
        result = run_adb_process([self.adb_path, "devices"], text=True)
        rows = result.stdout.splitlines()[1:]
        return [row.split()[0] for row in rows if "\tdevice" in row]

    def connect(self) -> None:
        if self.device_serial not in self.list_devices():
            raise ADBError(f"device not found: {self.device_serial}")

    def swipe(self, x1: int, y1: int, x2: int, y2: int, ms: int) -> None:
        args = ["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms)]
        self.run(args)

    def tap(self, x: int, y: int) -> None:
        self.run(["shell", "input", "tap", str(x), str(y)])

    def screenshot(self) -> np.ndarray:
        data = self.run_bytes(["exec-out", "screencap", "-p"])
        image = np.frombuffer(data, dtype=np.uint8)
        return cv2.imdecode(image, cv2.IMREAD_COLOR)

    def median_frame(self, count: int) -> np.ndarray:
        frames = self.capture_frames(count)
        stack = np.stack(frames, axis=0)
        return np.median(stack, axis=0).astype(np.uint8)

    def capture_frames(self, count: int) -> list[np.ndarray]:
        frames: list[np.ndarray] = []
        while len(frames) < count:
            append_decoded_frame(frames, self.screenshot())
        return frames


def append_decoded_frame(frames: list[np.ndarray], frame: np.ndarray) -> None:
    if frame is None:
        raise ADBError("截图解码失败")
    frames.append(frame)


def run_adb_process(command: list[str], text: bool = False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(command, capture_output=True, text=text, timeout=ADB_COMMAND_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as exc:
        raise ADBError(f"ADB 命令超时 {ADB_COMMAND_TIMEOUT_SECONDS} 秒: {format_adb_command(command)}") from exc


def format_adb_command(command: list[str]) -> str:
    return " ".join(command)
