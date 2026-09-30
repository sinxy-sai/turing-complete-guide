<div align="center">

# Turing Complete Guide

:video_game: Automation for the “Binary Speed Calculation” level in the standalone Turing Complete application.

<a href="https://github.com/sinxy-sai/turing-complete-guide"><img src="https://img.shields.io/badge/Turing%20Complete-2.1.334-4B5563?style=for-the-badge" alt="Turing Complete 2.1.334"></a>
<a href="https://www.microsoft.com/windows"><img src="https://img.shields.io/badge/Windows-10%2B-0078D6?logo=windows&logoColor=white&style=for-the-badge" alt="Windows 10 or later"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python 3.x"></a>
<a href="https://opencv.org/"><img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white&style=for-the-badge" alt="OpenCV 4.x"></a>
<a href="https://github.com/RapidAI/RapidOCR"><img src="https://img.shields.io/badge/RapidOCR-ONNX-FF6F00?style=for-the-badge" alt="RapidOCR ONNX"></a>
<a href="https://github.com/tesseract-ocr/tesseract"><img src="https://img.shields.io/badge/Tesseract-OCR-4285F4?style=for-the-badge" alt="Tesseract OCR fallback"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-750014?style=for-the-badge" alt="MIT License"></a>
<a href="docs/changelog.md"><img src="https://img.shields.io/badge/Changelog-view-6B7280?style=for-the-badge" alt="Changelog"></a>

**English** | [简体中文](README.zh-CN.md)

</div>

## :sparkles: Overview

This project captures the game screen, recognizes the decimal prompt, converts it to an 8-bit binary value, clicks the corresponding bit buttons, and submits the answer.

The project targets Windows desktop environments. Python dependencies are installed in the project-local `.venv`, and the OCR engine is installed in `.tools\tesseract`; system-wide Python packages and PATH configuration are not required.

<table>
  <tr>
    <td><strong>:desktop_computer: Platform</strong></td>
    <td>Windows 10 or later</td>
  </tr>
  <tr>
    <td><strong>:video_game: Interface</strong></td>
    <td>Standalone Turing Complete application</td>
  </tr>
  <tr>
    <td><strong>:label: Validated version</strong></td>
    <td>Turing Complete 2.1.334</td>
  </tr>
  <tr>
    <td><strong>:abc: OCR</strong></td>
    <td>RapidOCR for prompts; Tesseract OCR for Chinese dialogs and fallback</td>
  </tr>
  <tr>
    <td><strong>:page_facing_up: License</strong></td>
    <td><a href="LICENSE">MIT License</a></td>
  </tr>
</table>

> :warning: This is an independent learning and automation project. It is not affiliated with, sponsored by, or endorsed by the creators of Turing Complete.

## :rocket: Features

- :mag: Recognizes decimal prompts from the game screen.
- :art: Uses OpenCV to isolate orange digits and preprocess the image.
- :abc: Uses RapidOCR for prompt digits and Tesseract OCR for result-dialog recognition and fallback.
- :1234: Converts prompts to 8-bit binary and clicks the corresponding bit buttons.
- :octagonal_sign: Stops when a level-result dialog is detected and never clicks “Continue”.
- :hourglass_flowing_sand: Stops when the timeout page is detected instead of restarting the game.
- :test_tube: Provides screenshot regression tests and live diagnostic recording.

## :hammer_and_wrench: Installation

Run these commands from the repository root:

```powershell
.\automation\setup.ps1
.\automation\install-tesseract.ps1
```

The first command creates `.venv` and installs the Python dependencies. The second installs Tesseract OCR and the Simplified Chinese language data into `.tools\tesseract`.

## :arrow_forward: Usage

<details>
<summary>Show common commands</summary>

When the game shows the ready screen:

```powershell
.\automation\run.ps1 --fullscreen --wait-seconds 5
```

If the game is already showing a question, skip the Start action:

```powershell
.\automation\run.ps1 --fullscreen --no-start --wait-seconds 5
```

Run OCR without clicking an answer:

```powershell
.\automation\run.ps1 --fullscreen --no-start --dry-run --wait-seconds 5
```

Enable live diagnostics:

```powershell
.\automation\run.ps1 --fullscreen --wait-seconds 5 --diagnostics
```

Use `--window-title` when the window title differs from the default:

```powershell
.\automation\run.ps1 --window-title "Turing Complete" --no-start
```

</details>

Diagnostic data is written to `automation\tests\output\live\<timestamp>`. These generated files are ignored by Git.

## :test_tube: Tests

Run the screen-state regression tests:

```powershell
.\.venv\Scripts\python.exe automation\tests\test_states.py
```

Inspect preprocessing and OCR for a specific input:

```powershell
.\.venv\Scripts\python.exe automation\tests\test_preprocess_ocr.py automation\tests\input\81.png --expected 81
```

Input screenshots are stored in `automation\tests\input`. Generated test output is stored in `automation\tests\output` and is ignored by Git.

## :books: Documentation

See the [Binary Speedrun Automation Technical Documentation](docs/binary-speedrun.md) for the processing flow, state detection, OpenCV preprocessing, and OCR design.

See the [Changelog](docs/changelog.md) for the project development history.

## :file_folder: Project Structure

```text
.
├── automation/
│   ├── binary_speedrun.py       # Automation entry point
│   ├── run.ps1                  # Launcher
│   ├── setup.ps1                # Virtual environment and dependencies
│   ├── install-tesseract.ps1    # Project-local Tesseract installer
│   ├── requirements.txt         # Python dependencies
│   └── tests/
│       ├── input/               # Versioned screenshot fixtures
│       ├── output/              # Ignored generated test artifacts
│       ├── test_states.py
│       └── test_preprocess_ocr.py
├── docs/
│   └── binary-speedrun.md       # Technical documentation
├── README.md                    # English documentation
├── README.zh-CN.md              # Simplified Chinese documentation
└── LICENSE
```

## :page_facing_up: License

This project is licensed under the [MIT License](LICENSE). Please follow the terms in the repository's `LICENSE` file when using, modifying, or redistributing the project.

## :link: References

- Repository: [sinxy-sai/turing-complete-guide](https://github.com/sinxy-sai/turing-complete-guide)
- RapidOCR: [RapidAI/RapidOCR](https://github.com/RapidAI/RapidOCR)
- Tesseract OCR: [tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- Tesseract language data: [tessdata_fast](https://github.com/tesseract-ocr/tessdata_fast)
- OpenCV image processing documentation: [Image Processing in OpenCV](https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html)
- PyTesseract: [madmaze/pytesseract](https://github.com/madmaze/pytesseract)
- PyAutoGUI: [pyautogui.readthedocs.io](https://pyautogui.readthedocs.io/)
- Badge reference: [pudding0503/github-badge-collection](https://github.com/pudding0503/github-badge-collection)
