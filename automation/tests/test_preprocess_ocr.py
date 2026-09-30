"""Inspect OpenCV preprocessing and Tesseract OCR for a game screenshot."""

from __future__ import annotations

import sys
import argparse
from pathlib import Path

import cv2
import pytesseract
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "automation"))
import binary_speedrun as speedrun  # noqa: E402


def save_mask(path: Path, image) -> None:
    cv2.imwrite(str(path), image)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--expected", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    input_path = args.image.resolve()
    default_output = Path(__file__).with_name("output") / input_path.stem
    output = args.output or default_output
    output.mkdir(parents=True, exist_ok=True)
    source = Image.open(input_path).convert("RGB")
    box = speedrun.Box(0, 0, source.width, source.height)
    prompt = box.crop(source, 0.30, 0.30, 0.70, 0.56)
    prompt.save(output / "01_prompt_crop.png")

    warm, hsv, combined = speedrun.orange_digit_masks(prompt)
    save_mask(output / "02_warm_mask.png", warm)
    save_mask(output / "03_hsv_mask.png", hsv)
    save_mask(output / "04_combined_closed_mask.png", combined)

    processed = speedrun.orange_digit_image(prompt)
    if processed is None:
        (output / "results.txt").write_text("No orange digit region found.\n", encoding="utf-8")
        return 1
    processed.save(output / "05_tesseract_input.png")

    speedrun.configure_tesseract(None)
    rapid_text, rapid_number, rapid_confidence = speedrun.rapidocr_number(prompt)
    results: list[str] = []
    parsed_values: dict[int, int | None] = {}
    for psm in (7, 10, 8):
        text = pytesseract.image_to_string(
            processed,
            lang="eng",
            config=f"--psm {psm} -c tessedit_char_whitelist=0123456789",
        ).strip()
        parsed = speedrun.prompt_number(text)
        parsed_values[psm] = parsed
        results.append(f"psm={psm}: text={text!r}, parsed={parsed!r}")

    matching_psm = [psm for psm, value in parsed_values.items() if value == args.expected]

    report = [
        f"input={input_path}",
        f"expected={args.expected}",
        f"rapidocr: text={rapid_text!r}, parsed={rapid_number!r}, confidence={rapid_confidence:.3f}",
        *results,
        f"rapidocr_matching={rapid_number == args.expected}",
        f"matching_psm={matching_psm}",
        "Inspect 05_tesseract_input.png to verify the final OCR input image.",
    ]
    (output / "results.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
