<div align="center">

# Turing Complete Guide

:video_game: 用于自动完成 Turing Complete 独立应用“二进制速算”关卡的工具。

<a href="https://github.com/sinxy-sai/turing-complete-guide"><img src="https://img.shields.io/badge/Turing%20Complete-2.1.334-4B5563?style=flat-square" alt="Turing Complete 2.1.334"></a>
<a href="https://www.microsoft.com/windows"><img src="https://img.shields.io/badge/Windows-10%2B-0078D6?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI0YzNTMyNSIgZD0iTTEgMi43IDExIDEuM3YxMEgxeiIvPjxwYXRoIGZpbGw9IiM4MUJDMDYiIGQ9Ik0xMyAxIDIzIDB2MTFIMTN6Ii8%2BPHBhdGggZmlsbD0iIzA1QTZGMCIgZD0iTTEgMTNoMTB2MTBMMSAyMS43eiIvPjxwYXRoIGZpbGw9IiNGRkJBMDgiIGQ9Ik0xMyAxM2gxMHYxMWwtMTAtMS4zeiIvPjwvc3ZnPg%3D%3D" alt="Windows 10 或更高版本"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white&style=flat-square" alt="Python 3.x"></a>
<a href="https://opencv.org/"><img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white&style=flat-square" alt="OpenCV 4.x"></a>
<a href="https://github.com/RapidAI/RapidOCR"><img src="https://img.shields.io/badge/RapidOCR-ONNX-FF6F00?style=flat-square" alt="RapidOCR ONNX"></a>
<a href="LICENSE"><img src="https://img.shields.io/github/license/sinxy-sai/turing-complete-guide.svg?style=flat-square" alt="GitHub license"></a>
<a href="docs/changelog.md"><img src="https://img.shields.io/badge/Changelog-%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97-6B7280?style=flat-square" alt="更新日志"></a>
<a href="https://github.com/sinxy-sai/turing-complete-guide/stargazers"><img src="https://img.shields.io/github/stars/sinxy-sai/turing-complete-guide?style=flat-square&logo=github" alt="GitHub stars"></a>
<a href="https://github.com/sinxy-sai/turing-complete-guide/commits/main"><img src="https://img.shields.io/github/last-commit/sinxy-sai/turing-complete-guide?style=flat-square&logo=git" alt="最近提交"></a>

[English](README.md) | **简体中文**

</div>

<p align="center">
  <img
    src="https://socialify.git.ci/sinxy-sai/turing-complete-guide/image?description=1&font=Jost&forks=1&issues=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2Fsinxy-sai%2Fturing-complete-guide%2Fmain%2Fdocs%2Fassets%2Fbinary-speed-logo.svg&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark"
    alt="Turing Complete Guide Socialify 预览图"
    width="640"
  />
</p>

<p align="center">
  <a href="#installation">🚀 开始使用</a> ·
  <a href="#usage">▶️ 运行</a> ·
  <a href="#tests">🧪 测试</a> ·
  <a href="docs/binary-speedrun.md">📚 技术文档</a> ·
  <a href="docs/changelog.md">📝 更新日志</a>
</p>

## :sparkles: 项目简介

> **输入一张截图，输出一个正确的 8 位二进制答案。**

本项目通过屏幕截图识别游戏中的十进制题目，将数字转换为 8 位二进制表示，自动点击对应的位按钮并提交答案。

项目面向 Windows 桌面环境。Python 依赖（包括 RapidOCR ONNX Runtime）安装在项目内的 `.venv`，无需单独安装 OCR 可执行程序，也不要求修改系统 Python 或全局 PATH。

<table>
  <tr>
    <td><strong>:desktop_computer: 平台</strong></td>
    <td>Windows 10 或更高版本</td>
  </tr>
  <tr>
    <td><strong>:video_game: 运行环境</strong></td>
    <td>Turing Complete 独立应用</td>
  </tr>
  <tr>
    <td><strong>:link: Steam 商店</strong></td>
    <td><a href="https://store.steampowered.com/app/1444480/Turing_Complete/">在 Steam 购买 Turing Complete</a></td>
  </tr>
  <tr>
    <td><strong>:label: 开发与验证版本</strong></td>
    <td>Turing Complete 2.1.334</td>
  </tr>
  <tr>
    <td><strong>:abc: OCR</strong></td>
    <td>RapidOCR 识别题目数字和中文游戏状态文本</td>
  </tr>
  <tr>
    <td><strong>:page_facing_up: 许可证</strong></td>
    <td><a href="LICENSE">MIT License</a></td>
  </tr>
</table>

<p align="center">
  <sub>基于 Turing Complete 2.1.334 · Windows 桌面环境 · RapidOCR + OpenCV</sub>
</p>

> :warning: 本项目是独立的个人学习和自动化实验项目，与 Turing Complete 的开发者或发行方没有隶属、赞助或官方合作关系。

## :rocket: 主要功能

- :mag: 识别游戏界面中的十进制题目。
- :art: 使用 OpenCV 提取橙色数字并进行图像预处理。
- :abc: 使用 RapidOCR 识别题目数字和中文游戏状态文本。
- :1234: 转换为 8 位二进制并自动点击对应按钮。
- :stop_sign: 检测到等级结果弹窗后停止，不点击“继续”。
- :hourglass_flowing_sand: 检测到超时页面后停止，不重新启动游戏。
- :test_tube: 提供截图回归测试和实时诊断记录。

<a id="installation"></a>

## :hammer_and_wrench: 安装

在仓库根目录执行：

```powershell
.\automation\setup.ps1
```

该命令会创建 `.venv` 并安装 Python 依赖，包括 RapidOCR 和 ONNX Runtime。

<a id="usage"></a>

## :arrow_forward: 使用方法

<details>
<summary>展开常用命令</summary>

当游戏显示“准备好了吗？”时运行：

```powershell
.\automation\run.ps1 --fullscreen --wait-seconds 5
```

如果游戏已经进入题目界面，跳过开始操作：

```powershell
.\automation\run.ps1 --fullscreen --no-start --wait-seconds 5
```

只识别题目、不点击答案：

```powershell
.\automation\run.ps1 --fullscreen --no-start --dry-run --wait-seconds 5
```

开启实时诊断：

```powershell
.\automation\run.ps1 --fullscreen --wait-seconds 5 --diagnostics
```

窗口标题不同于默认值时，可以手动指定：

```powershell
.\automation\run.ps1 --window-title "Turing Complete" --no-start
```

</details>

诊断数据保存在 `automation\tests\output\live\<timestamp>`，并已加入 Git 忽略规则。
每次 OCR 尝试都会保存 `rapidocr_input.png` 和 `rapidocr_focus_input.png`，分别对应原始和彩色焦点裁剪图。

<a id="tests"></a>

## :test_tube: 测试

运行页面状态回归测试：

```powershell
.\.venv\Scripts\python.exe automation\tests\test_states.py
```

测试某个截图的 OpenCV 预处理和 OCR：

```powershell
.\.venv\Scripts\python.exe automation\tests\test_preprocess_ocr.py automation\tests\input\81.png --expected 81
```

回归样本中包括之前容易漏识别的 `0.png` 题目截图。

输入截图保存在 `automation\tests\input`，生成的测试结果保存在 `automation\tests\output`，后者不会提交到 Git。

## :books: 技术文档

详细的处理流程、状态判断、OpenCV 预处理和 OCR 设计见：[二进制速算自动化技术文档](docs/binary-speedrun.md)。

项目开发历史见：[Changelog 更新日志](docs/changelog.md)。

## :file_folder: 项目结构

```text
.
├── automation/
│   ├── binary_speed/            # 自动化 Python 包
│   │   ├── __main__.py          # python -m binary_speed 入口
│   │   ├── runner.py            # CLI 编排
│   │   ├── game.py              # 截图与游戏交互
│   │   ├── ocr.py               # OCR 服务
│   │   ├── vision.py            # OpenCV 预处理
│   │   ├── window.py            # 窗口选择
│   │   ├── diagnostics.py       # 可选诊断
│   │   └── models.py            # 公共数据模型
│   ├── run.ps1                  # 启动脚本
│   ├── setup.ps1                # 创建虚拟环境并安装依赖
│   ├── requirements.txt         # Python 依赖
│   └── tests/
│       ├── input/               # 已提交的真实截图样本
│       ├── output/              # 被 Git 忽略的测试产物
│       ├── test_states.py
│       └── test_preprocess_ocr.py
├── docs/
│   ├── assets/
│   │   └── binary-speed-logo.svg # Socialify 项目 Logo
│   └── binary-speedrun.md       # 技术文档
├── README.md                    # 英文文档
├── README.zh-CN.md              # 简体中文文档
└── LICENSE
```

## :page_facing_up: 许可证

本项目采用 [MIT License](LICENSE) 授权。使用、修改和分发本项目时，请遵守仓库根目录 `LICENSE` 文件中的条款。

## :link: 参考来源

- 项目仓库：[sinxy-sai/turing-complete-guide](https://github.com/sinxy-sai/turing-complete-guide)
- 游戏商店页面：[Steam 上的 Turing Complete](https://store.steampowered.com/app/1444480/Turing_Complete/)
- RapidOCR：[RapidAI/RapidOCR](https://github.com/RapidAI/RapidOCR)
- OpenCV 图像处理文档：[Image Processing in OpenCV](https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html)
- PyAutoGUI：[pyautogui.readthedocs.io](https://pyautogui.readthedocs.io/)
- Badge 参考：[pudding0503/github-badge-collection](https://github.com/pudding0503/github-badge-collection)
