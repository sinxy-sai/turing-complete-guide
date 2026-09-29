# Turing Complete 二进制速算自动化

脚本直接使用成熟库完成窗口定位、截图、点击和 OCR：`pygetwindow`、`pyautogui`、`Pillow`、`pytesseract`。识别到等级结果弹窗后会停止，不会点击“继续”。

项目使用根目录 `.venv` 管理依赖。首次初始化并安装：

```powershell
.\automation\setup.ps1
```

安装项目内的 Tesseract OCR：

```powershell
.\automation\install-tesseract.ps1
```

它会安装到 `.tools\tesseract`，并下载中文简体 OCR 数据。Python 脚本会自动优先使用项目内的版本。也可以手动指定其他路径：

```powershell
.\.venv\Scripts\python.exe .\automation\binary_speedrun.py --tesseract-cmd "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

游戏已打开时运行：

```powershell
.\automation\run.ps1
```

如果窗口标题无法被 Python 读取，但游戏已经全屏显示（你截图中的情况），点击任务栏最右侧的游戏图标后运行：

```powershell
.\automation\run.ps1 --fullscreen --no-start --wait-seconds 5
```

它不会自行猜测任务栏图标；启动后会倒计时，期间请点击任务栏最右侧图标切到游戏。数字识别会只提取题目中橙色的目标数字，避免把“第 1 级”和倒计时一起识别。

如果已经手动点击“开始”：

```powershell
.\automation\run.ps1 --no-start
```

建议先做只识别、不点击的测试：

```powershell
.\automation\run.ps1 --no-start --dry-run
```

脚本按窗口比例使用你提供的布局坐标，支持窗口尺寸变化。默认匹配窗口标题中的 `Turing Complete` 或 `二进制速算`；如果独立 App 的标题不同，可指定：

```powershell
.\automation\run.ps1 --window-title "你的窗口标题" --no-start --dry-run
```
