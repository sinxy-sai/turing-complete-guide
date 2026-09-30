"""Regression-test the game's ready, prompt, result, and timeout pages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "automation"))
import binary_speedrun as speedrun  # noqa: E402


INPUT_DIR = Path(__file__).with_name("input")
OUTPUT_DIR = Path(__file__).with_name("output") / "states"


def expected_for(path: Path) -> dict[str, object]:
    if path.stem == "ready":
        return {"state": "ready"}
    if path.stem.startswith("prompt_"):
        return {"state": "prompt", "number": int(path.stem.split("_", 1)[1])}
    if path.stem.startswith("result_level"):
        return {"state": "result", "level": int(path.stem.split("level", 1)[1])}
    if path.stem.startswith("timeout_level"):
        return {"state": "timeout"}
    if path.stem.isdigit():
        return {"state": "prompt", "number": int(path.stem)}
    return {"state": "unknown"}


def classify(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("RGB")
    box = speedrun.Box(0, 0, image.width, image.height)
    speedrun.capture = lambda _: image
    speedrun.configure_tesseract(None)

    full_text = speedrun.ocr(image).strip()
    timeout = speedrun.timeout_page(box)
    level = speedrun.reached_level(full_text)

    if timeout:
        state = "timeout"
        number = None
    elif level is not None:
        state = "result"
        number = None
    elif re.search(r"准\s*备\s*好\s*了\s*吗|开\s*始", full_text):
        state = "ready"
        number = None
    else:
        prompt_text, number = speedrun.read_number(box)
        state = "prompt" if number is not None else "unknown"
        full_text = f"{full_text}\n[prompt OCR] {prompt_text}"

    actual = {"state": state}
    if level is not None:
        actual["level"] = level
    if number is not None:
        actual["number"] = number
    expected = expected_for(path)
    passed = all(actual.get(key) == value for key, value in expected.items())
    return {
        "file": path.name,
        "expected": expected,
        "actual": actual,
        "passed": passed,
        "ocr": full_text,
    }


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cases = sorted(INPUT_DIR.glob("*.png"))
    results = [classify(path) for path in cases]
    (OUTPUT_DIR / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        f"{'PASS' if item['passed'] else 'FAIL'} {item['file']}: "
        f"expected={item['expected']}, actual={item['actual']}"
        for item in results
    ]
    (OUTPUT_DIR / "results.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
