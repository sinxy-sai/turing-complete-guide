"""Inspect the OpenCV preprocessing pipeline using the 58 screenshot."""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import pytesseract
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "automation"))
import binary_speedrun as speedrun  # noqa: E402


INPUT = Path(__file__).with_name("input_58.png")
OUTPUT = Path(__file__).with_name("output_58")


def save_mask(path: Path, image) -> None:
    cv2.imwrite(str(path), image)


def main() -> int:
    OUTPUT.mkdir(exist_ok=True)
    source = Image.open(INPUT).convert("RGB")
    box = speedrun.Box(0, 0, source.width, source.height)
    prompt = box.crop(source, 0.30, 0.30, 0.70, 0.56)
    prompt.save(OUTPUT / "01_prompt_crop.png")

    warm, hsv, combined = speedrun.orange_digit_masks(prompt)
    save_mask(OUTPUT / "02_warm_mask.png", warm)
    save_mask(OUTPUT / "03_hsv_mask.png", hsv)
    save_mask(OUTPUT / "04_combined_closed_mask.png", combined)

    processed = speedrun.orange_digit_image(prompt)
    if processed is None:
        (OUTPUT / "results.txt").write_text("No orange digit region found.\n", encoding="utf-8")
        return 1
    processed.save(OUTPUT / "05_tesseract_input.png")

    speedrun.configure_tesseract(None)
    results: list[str] = []
    for psm in (7, 10, 8):
        text = pytesseract.image_to_string(
            processed,
            lang="eng",
            config=f"--psm {psm} -c tessedit_char_whitelist=0123456789",
        ).strip()
        results.append(f"psm={psm}: text={text!r}, parsed={speedrun.prompt_number(text)!r}")

    report = [
        f"input={INPUT}",
        "expected=58",
        *results,
        "Inspect 05_tesseract_input.png to verify whether the 8 keeps both closed holes.",
    ]
    (OUTPUT / "results.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
