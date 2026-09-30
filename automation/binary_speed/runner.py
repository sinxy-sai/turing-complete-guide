"""Command-line runner for the binary speed calculation automation."""

from __future__ import annotations

import argparse
import time

import pyautogui

from .diagnostics import DiagnosticRecorder
from .game import capture, click, solve, timeout_page
from .ocr import PromptOCR, full_screen_text, reached_level
from .window import select_game_box


def _terminal_state(screen, box) -> tuple[str, int | None]:
    """Classify one already captured frame without taking another screenshot."""
    if timeout_page(screen, box):
        return "timeout", None
    level = reached_level(full_screen_text(screen))
    if level is not None:
        return "result", level
    return "active", None


def _stop_for_terminal_state(
    diagnostics: DiagnosticRecorder,
    round_dir,
    round_number: int,
    screen,
    state: str,
    level: int | None,
    started: float,
    message: str,
    attempt: int | None = None,
) -> None:
    filename = "timeout.png" if state == "timeout" else "result.png"
    diagnostics.save_image(filename, screen, round_dir)
    event: dict[str, object] = {
        "round": round_number,
        "state": state,
        "elapsed_ms": round((time.perf_counter() - started) * 1000),
    }
    if level is not None:
        event["level"] = level
    if attempt is not None:
        event["attempt"] = attempt
    diagnostics.event(event)
    print(message)


def _record_timeout(
    diagnostics: DiagnosticRecorder,
    round_dir,
    round_number: int,
    screen,
    started: float,
    attempt: int | None = None,
) -> None:
    _stop_for_terminal_state(
        diagnostics,
        round_dir,
        round_number,
        screen,
        "timeout",
        None,
        started,
        "Detected timeout page; stopped without restarting.",
        attempt,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-start", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="保存每轮截图、OCR 输入图、OCR 原文和耗时到 automation/tests/output/live",
    )
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
    return parser


def run(args: argparse.Namespace) -> None:
    pyautogui.PAUSE = 0.03
    pyautogui.FAILSAFE = True
    box = select_game_box(args.window_title, args.fullscreen, args.wait_seconds)
    diagnostics = DiagnosticRecorder(args.diagnostics)
    prompt_ocr = PromptOCR()

    if not args.no_start:
        click(box, 0.500, 0.420)
        time.sleep(0.30)

    for round_number in range(1, 10_000):
        round_started = time.perf_counter()
        round_dir = diagnostics.round_dir(round_number)
        screen = capture(box)
        state, level = _terminal_state(screen, box)
        if state != "active":
            message = (
                "Detected timeout page; stopped without restarting."
                if state == "timeout"
                else f"Detected result dialog: level {level}; stopped without Continue."
            )
            _stop_for_terminal_state(
                diagnostics, round_dir, round_number, screen, state, level, round_started, message
            )
            return

        result = None
        for attempt in range(20):
            screen = capture(box)
            if timeout_page(screen, box):
                _record_timeout(
                    diagnostics, round_dir, round_number, screen, round_started, attempt + 1
                )
                return
            prompt_image = box.crop(screen, 0.30, 0.30, 0.70, 0.56)
            result = prompt_ocr.read(prompt_image)
            attempt_dir = round_dir / f"attempt_{attempt + 1:02d}" if round_dir is not None else None
            diagnostics.record_prompt(attempt_dir, screen, prompt_image, result)
            diagnostics.event({"round": round_number, "state": "ocr", "attempt": attempt + 1, "text": result.text, "number": result.number, "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
            if result.number is not None:
                break
            time.sleep(0.12)

        if result is None or result.number is None:
            screen = capture(box)
            state, level = _terminal_state(screen, box)
            if state != "active":
                message = (
                    "Detected timeout page; stopped without restarting."
                    if state == "timeout"
                    else f"Detected result dialog: level {level}; stopped without Continue."
                )
                _stop_for_terminal_state(
                    diagnostics, round_dir, round_number, screen, state, level, round_started, message
                )
                return
            diagnostics.save_image("ocr_failed.png", screen, round_dir)
            diagnostics.event({"round": round_number, "state": "ocr_failed", "text": result.text if result else "", "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
            raise RuntimeError(f"OCR could not read the prompt. OCR text was: {result.text if result else ''!r}")

        number = result.number
        bits = format(number, "08b")
        print(f"Round {round_number}: {number} -> {bits}")
        if args.dry_run:
            return

        solve(box, number)
        time.sleep(0.18)
        screen = capture(box)
        diagnostics.save_image("after_submit.png", screen, round_dir)
        diagnostics.event({"round": round_number, "state": "submitted", "number": number, "bits": bits, "elapsed_ms": round((time.perf_counter() - round_started) * 1000)})
        state, level = _terminal_state(screen, box)
        if state != "active":
            message = (
                "Detected timeout page; stopped without restarting."
                if state == "timeout"
                else f"Reached level {level}; stopped without Continue."
            )
            _stop_for_terminal_state(
                diagnostics, round_dir, round_number, screen, state, level, round_started, message
            )
            return


def main() -> None:
    run(build_parser().parse_args())
