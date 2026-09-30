"""Automate Turing Complete's Binary Speed Calculation level."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pyautogui
import pygetwindow as gw
import pytesseract
import cv2
import numpy as np
from PIL import Image

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:  # pragma: no cover - the setup script installs this dependency
    RapidOCR = None


_rapidocr = None


@dataclass(frozen=True)
class Box:
    left: int
    top: int
    width: int
    height: int

    def point(self, x_ratio: float, y_ratio: float) -> tuple[int, int]:
        return (round(self.left + self.width * x_ratio), round(self.top + self.height * y_ratio))

    def crop(self, image, left: float, top: float, right: float, bottom: float):
        return image.crop((round(self.width * left), round(self.height * top), round(self.width * right), round(self.height * bottom)))


def find_game_window(title_hint: str | None = None) -> tuple[object, Box]:
    titles = [title_hint] if title_hint else ["Turing Complete", "二进制速算"]
    windows = [
        w
        for w in gw.getAllWindows()
        if w.width > 0 and any(hint.lower() in (w.title or "").lower() for hint in titles)
    ]
    if len(windows) != 1:
        raise RuntimeError(
            f"Expected one game window matching {titles}; found {[w.title for w in windows]}"
        )
    window = windows[0]
    if window.isMinimized:
        window.restore()
    window.activate()
    time.sleep(0.25)
    return window, Box(window.left, window.top, window.width, window.height)


def full_screen_box() -> Box:
    width, height = pyautogui.size()
    return Box(0, 0, width, height)


def select_game_box(title_hint: str | None, fullscreen: bool, wait_seconds: float) -> Box:
    if not fullscreen:
        _, box = find_game_window(title_hint)
        return box

    try:
        _, box = find_game_window(title_hint)
        print("已找到并切换到 Turing Complete 窗口。")
        return box
    except RuntimeError:
        box = full_screen_box()
        if wait_seconds > 0:
            print(f"未找到窗口标题，请在 {wait_seconds:g} 秒内切到游戏窗口…")
            time.sleep(wait_seconds)
        return box


def ocr(image) -> str:
    return pytesseract.image_to_string(image, lang="eng+chi_sim", config="--psm 6")


def configure_tesseract(explicit_path: str | None) -> None:
    candidates = []
    if explicit_path:
        candidates.append(explicit_path)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates.append(os.path.join(project_root, ".tools", "tesseract", "tesseract.exe"))
    for candidate in candidates:
        if os.path.isfile(candidate):
            pytesseract.pytesseract.tesseract_cmd = candidate
            return


def normalize_digits(text: str) -> str:
    return text.translate(str.maketrans("０１２３４５６７８９", "0123456789"))


def reached_level(text: str) -> int | None:
    text = normalize_digits(text)
    if not re.search(r"达到|成绩|漂亮|恭喜", text):
        return None
    levels = [int(value) for value in re.findall(r"第\s*(\d{1,2})\s*级", text)]
    return max(levels) if levels else None


def prompt_number(text: str) -> int | None:
    for value in re.findall(r"(?<!\d)(?:0|[1-9]\d{0,2})(?!\d)", normalize_digits(text)):
        number = int(value)
        if 0 <= number <= 255:
            return number
    return None


def orange_digit_masks(image):
    """Return warm-color, HSV, and combined masks for the orange digits."""
    rgb = np.asarray(image.convert("RGB"))
    red, green, blue = (rgb[:, :, index].astype(np.int16) for index in range(3))

    # Use both absolute color and channel differences. The latter keeps dim
    # antialiased orange edge pixels that do not pass a strict RGB threshold.
    warm_mask = (
        (red > green + 8)
        & (red > blue + 20)
        & (red > 70)
    ).astype(np.uint8) * 255
    hsv = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2HSV)
    hsv_mask = cv2.inRange(hsv, np.array([0, 25, 60]), np.array([42, 255, 255]))
    mask = cv2.bitwise_or(warm_mask, hsv_mask)

    # Close tiny breaks in glyph strokes, but keep the two holes in an 8.
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=1)
    return warm_mask, hsv_mask, closed_mask


def orange_digit_image(image):
    """Extract orange digits while preserving antialiased strokes and holes."""
    _, _, mask = orange_digit_masks(image)

    points = cv2.findNonZero(mask)
    if points is None:
        return None
    left, top, width, height = cv2.boundingRect(points)
    margin = max(8, round(min(width, height) * 0.15))
    left = max(0, left - margin)
    top = max(0, top - margin)
    right = min(mask.shape[1], left + width + margin * 2)
    bottom = min(mask.shape[0], top + height + margin * 2)
    cropped = mask[top:bottom, left:right]
    cropped = cv2.copyMakeBorder(cropped, 6, 6, 8, 8, cv2.BORDER_CONSTANT, value=0)
    cropped = cv2.resize(cropped, None, fx=5, fy=5, interpolation=cv2.INTER_NEAREST)
    _, cropped = cv2.threshold(cropped, 127, 255, cv2.THRESH_BINARY)
    return Image.fromarray(cropped)


def orange_digit_count(image) -> int:
    """Count the independent digit glyphs in the orange prompt mask."""
    _, _, mask = orange_digit_masks(image)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return sum(cv2.contourArea(contour) >= 500 for contour in contours)


def capture(box: Box):
    return pyautogui.screenshot(region=(box.left, box.top, box.width, box.height))


def rapidocr_number(image) -> tuple[str, int | None, float]:
    """Recognize the orange prompt number with RapidOCR."""
    global _rapidocr
    if RapidOCR is None:
        return "", None, -1.0
    if _rapidocr is None:
        _rapidocr = RapidOCR()

    result, _ = _rapidocr(np.asarray(image.convert("RGB")))
    if not result:
        return "", None, -1.0

    _, _, orange_mask = orange_digit_masks(image)
    candidates = []
    for box_points, raw_text, confidence in result:
        text = normalize_digits(str(raw_text)).strip()
        number = prompt_number(text)
        if number is None or not re.fullmatch(r"\d{1,3}", text):
            continue
        points = np.asarray(box_points, dtype=np.float32)
        left = max(0, int(np.floor(points[:, 0].min())))
        top = max(0, int(np.floor(points[:, 1].min())))
        right = min(orange_mask.shape[1], int(np.ceil(points[:, 0].max())) + 1)
        bottom = min(orange_mask.shape[0], int(np.ceil(points[:, 1].max())) + 1)
        if right <= left or bottom <= top:
            continue
        region = orange_mask[top:bottom, left:right]
        orange_ratio = cv2.countNonZero(region) / max(1, region.size)
        candidates.append((orange_ratio, float(confidence), text, number))

    if not candidates:
        return "", None, -1.0
    _, confidence, text, number = max(candidates, key=lambda item: (item[0], item[1]))
    return text, number, confidence


def ocr_number(image, psm: int) -> tuple[str, int | None, float]:
    """Read a number and return its text, parsed value, and OCR confidence."""
    config = f"--psm {psm} -c tessedit_char_whitelist=0123456789"
    data = pytesseract.image_to_data(
        image, lang="eng", config=config, output_type=pytesseract.Output.DICT
    )
    recognized = [
        (text.strip(), float(confidence))
        for text, confidence in zip(data["text"], data["conf"])
        if text.strip()
    ]
    text = " ".join(item[0] for item in recognized)
    confidence = max((item[1] for item in recognized), default=-1.0)
    return text, prompt_number(text), confidence


def read_number(box: Box, diagnostic_dir: Path | None = None) -> tuple[str, int | None]:
    image = capture(box)
    prompt_image = box.crop(image, 0.30, 0.30, 0.70, 0.56)
    if diagnostic_dir is not None:
        diagnostic_dir.mkdir(parents=True, exist_ok=True)
        image.save(diagnostic_dir / "screen.png")
        prompt_image.save(diagnostic_dir / "prompt_crop.png")
    digit_image = orange_digit_image(prompt_image)
    if digit_image is not None:
        rapid_text, rapid_number, rapid_confidence = rapidocr_number(prompt_image)
        if rapid_number is not None:
            if diagnostic_dir is not None:
                prompt_image.save(diagnostic_dir / "rapidocr_input.png")
                (diagnostic_dir / "ocr_attempts.txt").write_text(
                    f"rapidocr: {rapid_text!r}, parsed={rapid_number!r}, confidence={rapid_confidence:.3f}\n",
                    encoding="utf-8",
                )
            return rapid_text, rapid_number

        if diagnostic_dir is not None:
            digit_image.save(diagnostic_dir / "tesseract_input.png")
        digit_count = orange_digit_count(prompt_image)
        attempts = []
        candidates: list[tuple[str, int, float, int]] = []
        for psm in (7, 10, 8):
            text, number, confidence = ocr_number(digit_image, psm)
            attempts.append((psm, text, number, confidence))
            if number is not None and len(str(number)) == digit_count:
                candidates.append((text, number, confidence, psm))

            if psm == 7 and candidates and confidence >= 60:
                break
            if psm == 10 and candidates and attempts[0][2] == number and confidence >= 60:
                break

        if candidates:
            baseline = candidates[0]
            selected = baseline
            if len(candidates) >= 2 and candidates[-1][3] == 8:
                fallback = candidates[-1]
                if fallback[2] > baseline[2]:
                    selected = fallback
            if diagnostic_dir is not None:
                (diagnostic_dir / "ocr_attempts.txt").write_text(
                    "\n".join(
                        f"psm={psm}: {text!r}, parsed={number!r}, confidence={confidence:.0f}"
                        for psm, text, number, confidence in attempts
                    )
                    + "\n",
                    encoding="utf-8",
                )
            return selected[0], selected[1]
        return " | ".join(item[1] for item in attempts), None

    # During the transition between rounds the prompt area can contain only
    # background/animation pixels.  OCR on that full crop may find unrelated
    # digits (for example a stray ``0``) and turn a blank frame into a wrong
    # answer.  Wait for the orange prompt region to appear instead.
    if diagnostic_dir is not None:
        (diagnostic_dir / "ocr_attempts.txt").write_text(
            "no orange digit region found; retrying\n", encoding="utf-8"
        )
    return "", None


class DiagnosticRecorder:
    def __init__(self, enabled: bool) -> None:
        self.root: Path | None = None
        if enabled:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            self.root = Path(__file__).with_name("tests") / "output" / "live" / stamp
            self.root.mkdir(parents=True, exist_ok=True)
            self.events_path = self.root / "events.jsonl"

    def round_dir(self, round_number: int) -> Path | None:
        if self.root is None:
            return None
        path = self.root / f"round_{round_number:04d}"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def event(self, data: dict[str, object]) -> None:
        if self.root is None:
            return
        with self.events_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(data, ensure_ascii=False) + "\n")

    def save_screen(self, name: str, box: Box, round_dir: Path | None = None) -> None:
        if self.root is None:
            return
        target_dir = round_dir or self.root
        target_dir.mkdir(parents=True, exist_ok=True)
        capture(box).save(target_dir / name)


def read_level_dialog(box: Box) -> int | None:
    return reached_level(ocr(capture(box)))


def timeout_page(box: Box) -> bool:
    """Return whether the game is showing its timeout page."""
    image = capture(box)
    timeout_pixels = 0
    for y in range(round(box.height * 0.48), round(box.height * 0.58)):
        for x in range(round(box.width * 0.44), round(box.width * 0.56)):
            red, green, blue = image.getpixel((x, y))[:3]
            timeout_pixels += red > 150 and green < 150 and blue < 150 and red > green * 1.20
    return timeout_pixels >= 500


def click(box: Box, x_ratio: float, y_ratio: float) -> None:
    pyautogui.click(*box.point(x_ratio, y_ratio))


def solve(box: Box, number: int) -> str:
    weights = (128, 64, 32, 16, 8, 4, 2, 1)
    button_x = (0.274, 0.333, 0.392, 0.450, 0.509, 0.567, 0.625, 0.684)
    for x_ratio, weight in zip(button_x, weights):
        if number & weight:
            click(box, x_ratio, 0.835)
            time.sleep(0.025)
    click(box, 0.500, 0.950)
    return format(number, "08b")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stop-at-level", type=int, default=4)
    parser.add_argument("--no-start", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="保存每轮截图、OpenCV 输入图、OCR 原文和耗时到 automation/tests/output/live",
    )
    parser.add_argument("--tesseract-cmd")
    parser.add_argument("--window-title", help="独立 App 窗口标题中的文字")
    parser.add_argument(
        "--fullscreen",
        action="store_true",
        help="按整块屏幕操作已打开的独立 App，不查找窗口标题",
    )
    parser.add_argument(
        "--wait-seconds",
        type=float,
        default=3.0,
        help="全屏模式启动后等待你切到游戏的秒数",
    )
    args = parser.parse_args()

    configure_tesseract(args.tesseract_cmd)
    pyautogui.PAUSE = 0.03
    pyautogui.FAILSAFE = True
    box = select_game_box(args.window_title, args.fullscreen, args.wait_seconds)
    diagnostics = DiagnosticRecorder(args.diagnostics)

    if not args.no_start:
        click(box, 0.500, 0.420)
        time.sleep(0.30)

    for round_number in range(1, 10_000):
        round_started = time.perf_counter()
        round_dir = diagnostics.round_dir(round_number)
        if timeout_page(box):
            diagnostics.save_screen("timeout.png", box, round_dir)
            diagnostics.event({"round": round_number, "state": "timeout", "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
            print("Detected timeout page; stopped without restarting.")
            return

        level = read_level_dialog(box)
        if level is not None:
            diagnostics.save_screen("result.png", box, round_dir)
            diagnostics.event({"round": round_number, "state": "result", "level": level, "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
            print(f"Detected result dialog: level {level}; stopped without Continue.")
            return

        number = None
        prompt_text = ""
        for attempt in range(20):
            if timeout_page(box):
                diagnostics.save_screen("timeout.png", box, round_dir)
                diagnostics.event({"round": round_number, "state": "timeout", "attempt": attempt + 1, "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
                print("Detected timeout page; stopped without restarting.")
                return
            attempt_dir = round_dir / f"attempt_{attempt + 1:02d}" if round_dir is not None else None
            prompt_text, number = read_number(box, attempt_dir)
            diagnostics.event({"round": round_number, "state": "ocr", "attempt": attempt + 1, "text": prompt_text, "number": number, "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
            if number is not None:
                break
            time.sleep(0.12)
        if number is None:
            if timeout_page(box):
                diagnostics.save_screen("timeout.png", box, round_dir)
                diagnostics.event({"round": round_number, "state": "timeout", "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
                print("Detected timeout page; stopped without restarting.")
                return
            diagnostics.save_screen("ocr_failed.png", box, round_dir)
            diagnostics.event({"round": round_number, "state": "ocr_failed", "text": prompt_text, "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
            raise RuntimeError(f"OCR could not read the prompt. OCR text was: {prompt_text!r}")

        bits = format(number, "08b")
        print(f"Round {round_number}: {number} -> {bits}")
        if args.dry_run:
            return

        solve(box, number)
        time.sleep(0.18)
        diagnostics.save_screen("after_submit.png", box, round_dir)
        diagnostics.event({"round": round_number, "state": "submitted", "number": number, "bits": bits, "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
        if timeout_page(box):
            diagnostics.save_screen("timeout.png", box, round_dir)
            diagnostics.event({"round": round_number, "state": "timeout", "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
            print("Detected timeout page; stopped without restarting.")
            return
        level = read_level_dialog(box)
        if level is not None:
            diagnostics.save_screen("result.png", box, round_dir)
            diagnostics.event({"round": round_number, "state": "result", "level": level, "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
            print(f"Reached level {level}; stopped without Continue.")
            return


if __name__ == "__main__":
    main()
