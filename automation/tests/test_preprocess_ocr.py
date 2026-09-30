"""Inspect OpenCV preprocessing and RapidOCR for a game screenshot."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "automation"))
from binary_speed.models import Box  # noqa: E402
from binary_speed.ocr import PromptOCR  # noqa: E402
from binary_speed.vision import orange_digit_masks  # noqa: E402


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
    box = Box(0, 0, source.width, source.height)
    prompt = box.crop(source, 0.30, 0.30, 0.70, 0.56)
    prompt.save(output / "01_prompt_crop.png")

    warm, hsv, combined = orange_digit_masks(prompt)
    save_mask(output / "02_warm_mask.png", warm)
    save_mask(output / "03_hsv_mask.png", hsv)
    save_mask(output / "04_combined_closed_mask.png", combined)

    text, number, confidence = PromptOCR().rapidocr_number(prompt)
    report = [
        f"input={input_path}",
        f"expected={args.expected}",
        f"rapidocr: text={text!r}, parsed={number!r}, confidence={confidence:.3f}",
        f"matching={number == args.expected}",
        "RapidOCR reads the original prompt crop; OpenCV masks are saved for inspection.",
    ]
    (output / "results.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 0 if args.expected is None or number == args.expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
