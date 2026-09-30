# Changelog

All notable changes to this project are documented here. The project does not have a published release tag yet; the current entries describe the development state of the repository.

## [Unreleased] — 2026-09-30

### Added

- Automated the Turing Complete “Binary Speed Calculation” level.
- Added project-local `.venv` setup and project-local Tesseract installation scripts.
- Added OpenCV preprocessing for orange prompt digits.
- Added RapidOCR ONNX Runtime for prompt digit recognition.
- Added live diagnostics for screenshots, OCR attempts, submitted answers, result dialogs, and timeout pages.
- Added regression fixtures and tests for ready, prompt, result, timeout, and OCR edge-case states.
- Added English and Simplified Chinese README files.
- Added MIT License documentation and technical references.

### Changed

- Tesseract fallback processing uses the `psm 7 → 10 → 8` sequence.
- Prompt digit recognition now prefers RapidOCR; Tesseract remains available as a fallback and for result-dialog text.
- Orange digit contour counts are used to reject truncated OCR results, such as reading `81` as `1`.
- Blank transition frames are ignored until an orange prompt region is visible.
- The README now documents Turing Complete version `2.1.334` and provides GitHub-style badges.

### Fixed

- Stop immediately when a level-result dialog is detected; the automation does not click “Continue”.
- Stop immediately when the timeout page is detected; the automation does not restart the game.
- Prevent unrelated digits from background animation frames from being submitted as answers.

### Compatibility

- Validated with Turing Complete `2.1.334`.
- Target platform: Windows 10 or later.

## Documentation

- The default project documentation is available in [README.md](../README.md).
- Simplified Chinese documentation is available in [README.zh-CN.md](../README.zh-CN.md).
