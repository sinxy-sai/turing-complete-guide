# Turing Complete 二进制速算自动化

脚本使用 `pygetwindow`、`pyautogui`、`Pillow` 和 `pytesseract`，自动读取题目数字、选择 8 位按钮、提交答案，并在检测到等级结果弹窗后停止，不点击“继续”。

## 初始化

项目依赖统一安装到根目录 `.venv`：

```powershell
.\automation\setup.ps1
.\automation\install-tesseract.ps1
```

Tesseract 会安装到项目内 `.tools\tesseract`，并下载 `chi_sim` 中文语言数据。脚本会自动优先使用项目内的 `tesseract.exe`。

## 运行

准备界面显示“准备好了吗？”时，运行：

```powershell
.\automation\run.ps1 --fullscreen --wait-seconds 5
```

脚本会尝试激活独立 App；如果当前环境无法读取窗口标题，会倒计时 5 秒，请点击任务栏最右侧的 Turing Complete 图标。随后脚本自动点击“开始”。

已经进入题目界面时，跳过“开始”：

```powershell
.\automation\run.ps1 --fullscreen --no-start --wait-seconds 5
```

第一次建议只测试识别、不点击：

```powershell
.\automation\run.ps1 --fullscreen --no-start --dry-run --wait-seconds 5
```

如果 Python 能读取游戏窗口标题，也可以不使用全屏模式：

```powershell
.\automation\run.ps1
```

标题不同可以手动指定：

```powershell
.\automation\run.ps1 --window-title "你的窗口标题" --no-start --dry-run
```

## 依赖说明

- `.venv`：Python 虚拟环境，不污染系统 Python。
- `.tools\tesseract`：项目内 OCR 引擎，不污染系统 PATH。
- `chi_sim.traineddata`：识别中文等级结果弹窗。
- OpenCV：当前版本不需要，数字区域使用 Pillow 的颜色分割预处理。

详细流程和技术设计见 [`docs/binary-speedrun.md`](../docs/binary-speedrun.md)。
