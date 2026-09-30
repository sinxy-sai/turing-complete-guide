"""Game-window discovery and screen-region selection."""

from __future__ import annotations

import time

import pyautogui
import pygetwindow as gw

from .models import Box


def find_game_window(title_hint: str | None = None) -> tuple[object, Box]:
    titles = [title_hint] if title_hint else ["Turing Complete", "二进制速算"]
    windows = [
        window
        for window in gw.getAllWindows()
        if window.width > 0
        and any(hint.lower() in (window.title or "").lower() for hint in titles)
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
