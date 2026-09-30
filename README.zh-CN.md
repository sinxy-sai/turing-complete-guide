<div align="center">

# Turing Complete Guide

:video_game: 用于自动完成 Turing Complete 独立应用“二进制速算”关卡的工具。

<a href="https://github.com/sinxy-sai/turing-complete-guide"><img src="https://img.shields.io/badge/Turing%20Complete-2.1.334-4B5563?style=for-the-badge" alt="Turing Complete 2.1.334"></a>
<a href="https://www.microsoft.com/windows"><img src="https://img.shields.io/badge/Windows-10%2B-0078D6?logo=windows&logoColor=white&style=for-the-badge" alt="Windows 10 或更高版本"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python 3.x"></a>
<a href="https://opencv.org/"><img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white&style=for-the-badge" alt="OpenCV 4.x"></a>
<a href="https://github.com/tesseract-ocr/tesseract"><img src="https://img.shields.io/badge/Tesseract-OCR-4285F4?style=for-the-badge" alt="Tesseract OCR"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-750014?style=for-the-badge" alt="MIT License"></a>
<a href="docs/changelog.md"><img src="https://img.shields.io/badge/Changelog-%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97-6B7280?style=for-the-badge" alt="更新日志"></a>

[English](README.md) | **简体中文**

</div>

## :sparkles: 项目简介

本项目通过屏幕截图识别游戏中的十进制题目，将数字转换为 8 位二进制表示，自动点击对应的位按钮并提交答案。

项目面向 Windows 桌面环境。Python 依赖安装在项目内的 `.venv`，OCR 引擎安装在 `.tools\tesseract`，不要求修改系统 Python 或全局 PATH。

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
    <td><strong>:label: 开发与验证版本</strong></td>
    <td>Turing Complete 2.1.334</td>
  </tr>
  <tr>
    <td><strong>:abc: OCR</strong></td>
    <td>Tesseract OCR 与简体中文语言数据</td>
  </tr>
  <tr>
    <td><strong>:page_facing_up: 许可证</strong></td>
    <td><a href="LICENSE">MIT License</a></td>
  </tr>
</table>

> :warning: 本项目是独立的个人学习和自动化实验项目，与 Turing Complete 的开发者或发行方没有隶属、赞助或官方合作关系。

## :rocket: 主要功能

- :mag: 识别游戏界面中的十进制题目。
- :art: 使用 OpenCV 提取橙色数字并进行图像预处理。
- :abc: 使用 Tesseract OCR 识别题目数字和结果弹窗。
- :1234: 转换为 8 位二进制并自动点击对应按钮。
- :octagonal_sign: 检测到等级结果弹窗后停止，不点击“继续”。
- :hourglass_flowing_sand: 检测到超时页面后停止，不重新启动游戏。
- :test_tube: 提供截图回归测试和实时诊断记录。

## :hammer_and_wrench: 安装

在仓库根目录执行：

```powershell
.\automation\setup.ps1
.\automation\install-tesseract.ps1
```

第一条命令会创建 `.venv` 并安装 Python 依赖。第二条命令会将 Tesseract OCR 和简体中文语言数据安装到项目内的 `.tools\tesseract`。

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

## :test_tube: 测试

运行页面状态回归测试：

```powershell
.\.venv\Scripts\python.exe automation\tests\test_states.py
```

测试某个截图的 OpenCV 预处理和 OCR：

```powershell
.\.venv\Scripts\python.exe automation\tests\test_preprocess_ocr.py automation\tests\input\81.png --expected 81
```

输入截图保存在 `automation\tests\input`，生成的测试结果保存在 `automation\tests\output`，后者不会提交到 Git。

## :books: 技术文档

详细的处理流程、状态判断、OpenCV 预处理和 OCR 设计见：[二进制速算自动化技术文档](docs/binary-speedrun.md)。

项目开发历史见：[Changelog 更新日志](docs/changelog.md)。

## :file_folder: 项目结构

```text
.
├── automation/
│   ├── binary_speedrun.py       # 自动化主程序
│   ├── run.ps1                  # 启动脚本
│   ├── setup.ps1                # 创建虚拟环境并安装依赖
│   ├── install-tesseract.ps1    # 安装项目内 Tesseract
│   ├── requirements.txt         # Python 依赖
│   └── tests/
│       ├── input/               # 已提交的真实截图样本
│       ├── output/              # 被 Git 忽略的测试产物
│       ├── test_states.py
│       └── test_preprocess_ocr.py
├── docs/
│   └── binary-speedrun.md       # 技术文档
├── README.md                    # 英文文档
├── README.zh-CN.md              # 简体中文文档
└── LICENSE
```

## :page_facing_up: 许可证

本项目采用 [MIT License](LICENSE) 授权。使用、修改和分发本项目时，请遵守仓库根目录 `LICENSE` 文件中的条款。

## :link: 参考来源

- 项目仓库：[sinxy-sai/turing-complete-guide](https://github.com/sinxy-sai/turing-complete-guide)
- Tesseract OCR：[tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- Tesseract 语言数据：[tessdata_fast](https://github.com/tesseract-ocr/tessdata_fast)
- OpenCV 图像处理文档：[Image Processing in OpenCV](https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html)
- PyTesseract：[madmaze/pytesseract](https://github.com/madmaze/pytesseract)
- PyAutoGUI：[pyautogui.readthedocs.io](https://pyautogui.readthedocs.io/)
- Badge 参考：[pudding0503/github-badge-collection](https://github.com/pudding0503/github-badge-collection)
