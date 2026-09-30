"""OpenCV preprocessing for the orange prompt digits."""

from __future__ import annotations

import cv2
import numpy as np


def orange_digit_masks(image):
    """Return warm-color, HSV, and combined masks for the orange digits."""
    rgb = np.asarray(image.convert("RGB"))
    red, green, blue = (rgb[:, :, index].astype(np.int16) for index in range(3))

    warm_mask = (
        (red > green + 8)
        & (red > blue + 20)
        & (red > 70)
    ).astype(np.uint8) * 255
    hsv = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2HSV)
    hsv_mask = cv2.inRange(hsv, np.array([0, 25, 60]), np.array([42, 255, 255]))
    mask = cv2.bitwise_or(warm_mask, hsv_mask)

    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=1)
    return warm_mask, hsv_mask, closed_mask
