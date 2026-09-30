"""OCR services for prompt digits and result dialogs."""

from __future__ import annotations

import os
import re
from pathlib import Path

import cv2
import numpy as np
import pytesseract

from .models import OCRAttempt, PromptRead
from .vision import orange_digit_count, orange_digit_image, orange_digit_masks

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:  # pragma: no cover - setup installs this dependency
    RapidOCR = None


def configure_tesseract(explicit_path: str | None) -> None:
    candidates = []
    if explicit_path:
        candidates.append(explicit_path)
    project_root = Path(__file__).resolve().parents[2]
    candidates.append(project_root / ".tools" / "tesseract" / "tesseract.exe")
    for candidate in candidates:
        if os.path.isfile(candidate):
            pytesseract.pytesseract.tesseract_cmd = str(candidate)
            return


def full_screen_text(image) -> str:
    return pytesseract.image_to_string(image, lang="eng+chi_sim", config="--psm 6")


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
    """Read prompt digits with RapidOCR and fall back to Tesseract."""

    def __init__(self) -> None:
        self._rapidocr = None

    def _rapidocr_engine(self):
        if RapidOCR is None:
            return None
        if self._rapidocr is None:
            self._rapidocr = RapidOCR()
        return self._rapidocr

    def rapidocr_number(self, image) -> tuple[str, int | None, float]:
        engine = self._rapidocr_engine()
        if engine is None:
            return "", None, -1.0

        result, _ = engine(np.asarray(image.convert("RGB")))
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

    def tesseract_number(self, image, psm: int) -> tuple[str, int | None, float]:
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

    def read(self, prompt_image) -> PromptRead:
        digit_image = orange_digit_image(prompt_image)
        if digit_image is None:
            return PromptRead(prompt_image=prompt_image)

        rapid_text, rapid_number, rapid_confidence = self.rapidocr_number(prompt_image)
        if rapid_number is not None:
            return PromptRead(
                text=rapid_text,
                number=rapid_number,
                attempts=[OCRAttempt("rapidocr", rapid_text, rapid_number, rapid_confidence)],
                digit_image=digit_image,
                prompt_image=prompt_image,
            )

        digit_count = orange_digit_count(prompt_image)
        attempts: list[OCRAttempt] = []
        candidates: list[tuple[OCRAttempt, int]] = []
        for psm in (7, 10, 8):
            text, number, confidence = self.tesseract_number(digit_image, psm)
            attempt = OCRAttempt("tesseract", text, number, confidence, psm)
            attempts.append(attempt)
            if number is not None and len(str(number)) == digit_count:
                candidates.append((attempt, psm))

            if psm == 7 and candidates and confidence >= 60:
                break
            if psm == 10 and candidates and attempts[0].number == number and confidence >= 60:
                break

        if not candidates:
            return PromptRead(
                text=" | ".join(attempt.text for attempt in attempts),
                attempts=attempts,
                digit_image=digit_image,
                prompt_image=prompt_image,
            )

        baseline = candidates[0][0]
        selected = baseline
        if candidates[-1][0].mode == 8 and candidates[-1][0].confidence > baseline.confidence:
            selected = candidates[-1][0]
        return PromptRead(
            text=selected.text,
            number=selected.number,
            attempts=attempts,
            digit_image=digit_image,
            prompt_image=prompt_image,
        )
