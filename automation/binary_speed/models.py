"""Shared data models used by the automation layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Box:
    left: int
    top: int
    width: int
    height: int

    def point(self, x_ratio: float, y_ratio: float) -> tuple[int, int]:
        return (
            round(self.left + self.width * x_ratio),
            round(self.top + self.height * y_ratio),
        )

    def crop(self, image: Any, left: float, top: float, right: float, bottom: float):
        return image.crop(
            (
                round(self.width * left),
                round(self.height * top),
                round(self.width * right),
                round(self.height * bottom),
            )
        )


@dataclass(frozen=True)
class OCRAttempt:
    engine: str
    text: str
    number: int | None
    confidence: float


@dataclass
class PromptRead:
    text: str = ""
    number: int | None = None
    attempts: list[OCRAttempt] = field(default_factory=list)
    prompt_image: Any | None = None
