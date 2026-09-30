"""OpenCV preprocessing for the orange prompt digits."""

from __future__ import annotations

import cv2
import numpy as np
from PIL import Image


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


def orange_digit_image(image):
    """Extract orange digits for the Tesseract fallback."""
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
    """Count independent digit glyphs in the orange prompt mask."""
    _, _, mask = orange_digit_masks(image)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return sum(cv2.contourArea(contour) >= 500 for contour in contours)
