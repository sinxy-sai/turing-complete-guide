<div align="center">

# Turing Complete Guide

:video_game: Automation for the “Binary Speed Calculation” level in the standalone Turing Complete application.

<a href="https://github.com/sinxy-sai/turing-complete-guide"><img src="https://img.shields.io/badge/Turing%20Complete-2.1.334-4B5563?style=flat-square" alt="Turing Complete 2.1.334"></a>
<a href="https://www.microsoft.com/windows"><img src="https://img.shields.io/badge/Windows-10%2B-0078D6?logo=windows&logoColor=white&style=flat-square" alt="Windows 10 or later"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white&style=flat-square" alt="Python 3.x"></a>
<a href="https://opencv.org/"><img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white&style=flat-square" alt="OpenCV 4.x"></a>
<a href="https://github.com/RapidAI/RapidOCR"><img src="https://img.shields.io/badge/RapidOCR-ONNX-FF6F00?style=flat-square" alt="RapidOCR ONNX"></a>
<a href="LICENSE"><img src="https://img.shields.io/github/license/sinxy-sai/turing-complete-guide.svg?style=flat-square" alt="GitHub license"></a>
<a href="docs/changelog.md"><img src="https://img.shields.io/badge/Changelog-view-6B7280?style=flat-square" alt="Changelog"></a>
<a href="https://github.com/sinxy-sai/turing-complete-guide/stargazers"><img src="https://img.shields.io/github/stars/sinxy-sai/turing-complete-guide?style=flat-square&logo=github" alt="GitHub stars"></a>
<a href="https://github.com/sinxy-sai/turing-complete-guide/commits/main"><img src="https://img.shields.io/github/last-commit/sinxy-sai/turing-complete-guide?style=flat-square&logo=git" alt="Last commit"></a>

**English** | [简体中文](README.zh-CN.md)

</div>

<p align="center">
  <img
    src="https://socialify.git.ci/sinxy-sai/turing-complete-guide/image?description=1&font=Jost&forks=1&issues=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2Fsinxy-sai%2Fturing-complete-guide%2Fmain%2Fdocs%2Fassets%2Fbinary-speed-logo.svg&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark"
    alt="Turing Complete Guide Socialify preview"
    width="640"
  />
</p>

<p align="center">
  <a href="#installation">🚀 Get Started</a> ·
  <a href="#usage">▶️ Run</a> ·
  <a href="#tests">🧪 Test</a> ·
  <a href="docs/binary-speedrun.md">📚 Documentation</a> ·
  <a href="docs/changelog.md">📝 Changelog</a>
</p>

## :sparkles: Overview

> **One screenshot in, one correct 8-bit answer out.**

This project captures the game screen, recognizes the decimal prompt, converts it to an 8-bit binary value, clicks the corresponding bit buttons, and submits the answer.

The project targets Windows desktop environments. Python dependencies, including the RapidOCR ONNX runtime, are installed in the project-local `.venv`; no separate OCR executable or system-wide Python packages are required.

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
    <td>RapidOCR for prompt digits and Chinese game-state text</td>
  </tr>
  <tr>
    <td><strong>:page_facing_up: License</strong></td>
    <td><a href="LICENSE">MIT License</a></td>
  </tr>
</table>

<p align="center">
  <sub>Built for Turing Complete 2.1.334 · Windows desktop · RapidOCR + OpenCV</sub>
</p>

> :warning: This is an independent learning and automation project. It is not affiliated with, sponsored by, or endorsed by the creators of Turing Complete.

## :rocket: Features

- :mag: Recognizes decimal prompts from the game screen.
- :art: Uses OpenCV to isolate orange digits and preprocess the image.
- :abc: Uses RapidOCR for prompt digits and Chinese game-state text.
- :1234: Converts prompts to 8-bit binary and clicks the corresponding bit buttons.
- :octagonal_sign: Stops when a level-result dialog is detected and never clicks “Continue”.
- :hourglass_flowing_sand: Stops when the timeout page is detected instead of restarting the game.
- :test_tube: Provides screenshot regression tests and live diagnostic recording.

<a id="installation"></a>

## :hammer_and_wrench: Installation

Run these commands from the repository root:

```powershell
.\automation\setup.ps1
```

The setup command creates `.venv` and installs the Python dependencies, including RapidOCR and its ONNX runtime.

<a id="usage"></a>

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
Each OCR attempt records both `rapidocr_input.png` and `rapidocr_focus_input.png`, representing the original and focused color crops.

<a id="tests"></a>

## :test_tube: Tests

Run the screen-state regression tests:

```powershell
.\.venv\Scripts\python.exe automation\tests\test_states.py
```

Inspect preprocessing and OCR for a specific input:

```powershell
.\.venv\Scripts\python.exe automation\tests\test_preprocess_ocr.py automation\tests\input\81.png --expected 81
```

The regression fixtures include the previously problematic `0.png` prompt.

Input screenshots are stored in `automation\tests\input`. Generated test output is stored in `automation\tests\output` and is ignored by Git.

## :books: Documentation

See the [Binary Speedrun Automation Technical Documentation](docs/binary-speedrun.md) for the processing flow, state detection, OpenCV preprocessing, and OCR design.

See the [Changelog](docs/changelog.md) for the project development history.

## :file_folder: Project Structure

```text
.
├── automation/
│   ├── binary_speed/            # Automation package
│   │   ├── __main__.py          # python -m binary_speed entry point
│   │   ├── runner.py            # CLI orchestration
│   │   ├── game.py              # Capture and game interaction
│   │   ├── ocr.py               # OCR services
│   │   ├── vision.py            # OpenCV preprocessing
│   │   ├── window.py            # Window selection
│   │   ├── diagnostics.py       # Optional diagnostics
│   │   └── models.py            # Shared data models
│   ├── run.ps1                  # Launcher
│   ├── setup.ps1                # Virtual environment and dependencies
│   ├── requirements.txt         # Python dependencies
│   └── tests/
│       ├── input/               # Versioned screenshot fixtures
│       ├── output/              # Ignored generated test artifacts
│       ├── test_states.py
│       └── test_preprocess_ocr.py
├── docs/
│   ├── assets/
│   │   └── binary-speed-logo.svg # Socialify project logo
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
- OpenCV image processing documentation: [Image Processing in OpenCV](https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html)
- PyAutoGUI: [pyautogui.readthedocs.io](https://pyautogui.readthedocs.io/)
- Badge reference: [pudding0503/github-badge-collection](https://github.com/pudding0503/github-badge-collection)
