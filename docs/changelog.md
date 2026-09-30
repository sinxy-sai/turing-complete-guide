# Changelog

All notable changes to this project are documented here. The project does not have a published release tag yet; the current entries describe the development state of the repository.

## [Unreleased] — 2026-09-30

### Added

- Automated the Turing Complete “Binary Speed Calculation” level.
- Added project-local `.venv` setup and dependency installation scripts.
- Added OpenCV preprocessing for orange prompt digits.
- Added RapidOCR ONNX Runtime for prompt digit recognition.
- Added live diagnostics for screenshots, OCR attempts, submitted answers, result dialogs, and timeout pages.
- Added regression fixtures and tests for ready, prompt, result, timeout, and OCR edge-case states.
- Added the real `0.png` regression fixture for a prompt that previously disappeared during live OCR.
- Added English and Simplified Chinese README files.
- Added MIT License documentation and technical references.

### Changed

- RapidOCR now checks both the original prompt crop and a narrower central focus crop.
- Live diagnostics now save both RapidOCR input images.
- Blank transition frames are ignored until an orange prompt region is visible.
- The README now documents Turing Complete version `2.1.334` and provides GitHub-style badges.

### Fixed

- Fixed the live OCR failure for the real `0` prompt sample; the sample and a full level-7 run now pass.
- Stop immediately when a level-result dialog is detected; the automation does not click “Continue”.
- Stop immediately when the timeout page is detected; the automation does not restart the game.
- Prevent unrelated digits from background animation frames from being submitted as answers.

### Removed

- The project initially used Tesseract OCR through PyTesseract. It was used for Chinese result-dialog and timeout-state text, and as a `psm 7 → 10 → 8` fallback for prompt digits.
- Tesseract was removed after RapidOCR was validated against the prompt fixtures, Chinese state pages, the `0` regression sample, and a complete level-7 run. This removed the separate executable, language-data download, and project-local installation step while keeping the recognition workflow in one OCR engine.

### Compatibility

- Validated with Turing Complete `2.1.334`.
- Target platform: Windows 10 or later.

## Documentation

- The default project documentation is available in [README.md](../README.md).
- Simplified Chinese documentation is available in [README.zh-CN.md](../README.zh-CN.md).
