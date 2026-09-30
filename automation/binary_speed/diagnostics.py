"""Optional live diagnostic recording, kept outside the automation core."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import PromptRead
from .vision import prompt_focus


class DiagnosticRecorder:
    def __init__(self, enabled: bool) -> None:
        self.root: Path | None = None
        if enabled:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            self.root = Path(__file__).resolve().parents[1] / "tests" / "output" / "live" / stamp
            self.root.mkdir(parents=True, exist_ok=True)
            self.events_path = self.root / "events.jsonl"

    def round_dir(self, round_number: int) -> Path | None:
        if self.root is None:
            return None
        path = self.root / f"round_{round_number:04d}"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def event(self, data: dict[str, object]) -> None:
        if self.root is None:
            return
        with self.events_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(data, ensure_ascii=False) + "\n")

    def record_prompt(
        self,
        attempt_dir: Path | None,
        screen,
        prompt_image,
        result: PromptRead,
    ) -> None:
        if self.root is None or attempt_dir is None:
            return
        attempt_dir.mkdir(parents=True, exist_ok=True)
        screen.save(attempt_dir / "screen.png")
        prompt_image.save(attempt_dir / "prompt_crop.png")
        if result.prompt_image is not None:
            prompt_image.save(attempt_dir / "rapidocr_input.png")
            prompt_focus(prompt_image).save(attempt_dir / "rapidocr_focus_input.png")
        lines = []
        for attempt in result.attempts:
            lines.append(
                f"{attempt.engine}: {attempt.text!r}, parsed={attempt.number!r}, confidence={attempt.confidence:.3f}"
            )
        (attempt_dir / "ocr_attempts.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def save_image(self, name: str, image, round_dir: Path | None = None) -> None:
        """Save an already captured frame without taking a second screenshot."""
        if self.root is None:
            return
        target_dir = round_dir or self.root
        target_dir.mkdir(parents=True, exist_ok=True)
        image.save(target_dir / name)
