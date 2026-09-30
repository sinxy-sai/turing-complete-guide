"""OCR services for prompt digits and result dialogs."""

from __future__ import annotations

import re

import cv2
import numpy as np

from .models import OCRAttempt, PromptRead
from .vision import orange_digit_masks, prompt_focus

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:  # pragma: no cover - setup installs this dependency
    RapidOCR = None


_rapidocr = None


def _rapidocr_engine():
    global _rapidocr
    if RapidOCR is None:
        return None
    if _rapidocr is None:
        _rapidocr = RapidOCR()
    return _rapidocr


def full_screen_text(image) -> str:
    """Return all text detected by RapidOCR on a full game frame."""
    engine = _rapidocr_engine()
    if engine is None:
        return ""
    result, _ = engine(np.asarray(image.convert("RGB")))
    return " ".join(str(item[1]) for item in (result or []))


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


class PromptOCR:
    """Read orange prompt digits with RapidOCR."""

    def rapidocr_number(self, image) -> tuple[str, int | None, float]:
        engine = _rapidocr_engine()
        if engine is None:
            return "", None, -1.0

        candidates = []
        for source in (image, prompt_focus(image)):
            result, _ = engine(np.asarray(source.convert("RGB")))
            if not result:
                continue
            _, _, orange_mask = orange_digit_masks(source)
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

    def read(self, prompt_image) -> PromptRead:
        rapid_text, rapid_number, rapid_confidence = self.rapidocr_number(prompt_image)
        return PromptRead(
            text=rapid_text,
            number=rapid_number,
            attempts=[OCRAttempt("rapidocr", rapid_text, rapid_number, rapid_confidence)],
            prompt_image=prompt_image,
        )
