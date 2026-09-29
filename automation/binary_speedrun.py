"""Automate Turing Complete's Binary Speed Calculation level."""

from __future__ import annotations

import argparse
import os
import re
import time
from dataclasses import dataclass

import pyautogui
import pygetwindow as gw
import pytesseract


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


def orange_digit_image(image):
    """Keep only the orange decimal target and remove surrounding UI text."""
    pixels = image.load()
    values = []
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue = pixels[x, y][:3]
            is_orange = (
                red > 150
                and 60 < green < 220
                and blue < 150
                and red > green * 1.15
                and red > blue * 1.30
            )
            values.append(255 if is_orange else 0)

    from PIL import Image

    mask = Image.new("L", image.size, 0)
    mask.putdata(values)
    bounds = mask.getbbox()
    if bounds is None:
        return None
    left, top, right, bottom = bounds
    margin = 10
    cropped = mask.crop(
        (
            max(0, left - margin),
            max(0, top - margin),
            min(mask.width, right + margin),
            min(mask.height, bottom + margin),
        )
    )
    return cropped.resize((cropped.width * 4, cropped.height * 4))


def capture(box: Box):
    return pyautogui.screenshot(region=(box.left, box.top, box.width, box.height))


def read_number(box: Box) -> tuple[str, int | None]:
    image = capture(box)
    prompt_image = box.crop(image, 0.30, 0.30, 0.70, 0.56)
    digit_image = orange_digit_image(prompt_image)
    if digit_image is not None:
        attempts = []
        for psm in (7, 10, 8):
            text = pytesseract.image_to_string(
                digit_image,
                lang="eng",
                config=f"--psm {psm} -c tessedit_char_whitelist=0123456789",
            ).strip()
            attempts.append(text)
            number = prompt_number(text)
            if number is not None:
                return text, number
        return " | ".join(attempts), None

    text = ocr(prompt_image)
    return text, prompt_number(text)


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

    if not args.no_start:
        click(box, 0.500, 0.420)
        time.sleep(0.30)

    for round_number in range(1, 10_000):
        if timeout_page(box):
            print("Detected timeout page; stopped without restarting.")
            return

        level = read_level_dialog(box)
        if level is not None:
            print(f"Detected result dialog: level {level}; stopped without Continue.")
            return

        number = None
        prompt_text = ""
        for _ in range(20):
            if timeout_page(box):
                print("Detected timeout page; stopped without restarting.")
                return
            prompt_text, number = read_number(box)
            if number is not None:
                break
            time.sleep(0.12)
        if number is None:
            if timeout_page(box):
                print("Detected timeout page; stopped without restarting.")
                return
            raise RuntimeError(f"OCR could not read the prompt. OCR text was: {prompt_text!r}")

        bits = format(number, "08b")
        print(f"Round {round_number}: {number} -> {bits}")
        if args.dry_run:
            return

        solve(box, number)
        time.sleep(0.18)
        if timeout_page(box):
            print("Detected timeout page; stopped without restarting.")
            return
        level = read_level_dialog(box)
        if level is not None:
            print(f"Reached level {level}; stopped without Continue.")
            return


if __name__ == "__main__":
    main()
