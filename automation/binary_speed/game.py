"""Screen capture, game-state pixels, and binary-answer interactions."""

from __future__ import annotations

import time

import pyautogui

from .models import Box


def capture(box: Box):
    return pyautogui.screenshot(region=(box.left, box.top, box.width, box.height))


def timeout_page(image, box: Box) -> bool:
    """Return whether the supplied game image shows the timeout page."""
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
