# OpenCV 预处理与 OCR 测试

使用 `input` 目录中的游戏截图，验证二进制速算题目的 OpenCV 预处理、RapidOCR 主识别和 Tesseract 备用 OCR。

自动化实现位于 `automation/binary_speed` Python 包中；`run.ps1` 通过 `python -m binary_speed` 启动，不再保留单文件兼容入口。

运行：

```powershell
.\.venv\Scripts\python.exe automation\tests\test_preprocess_ocr.py automation\tests\input\58.png --expected 58
.\.venv\Scripts\python.exe automation\tests\test_preprocess_ocr.py automation\tests\input\79.png --expected 79
```

页面状态回归测试：

```powershell
.\.venv\Scripts\python.exe automation\tests\test_states.py
```

它会测试 `ready`、普通题目、等级结果弹窗和超时页面，并将状态与 OCR 原文写入 `output\states\results.json` 和 `results.txt`。超时页面中即使还能识别到等级文字，也按 timeout 分类，因为超时应立即终止自动化。

当前输入样本包括：

- `ready.png`：准备页面，包含“准备好了吗？”和“开始”。
- `prompt_1.png`、`58.png`、`79.png`：题目页面。
- `57.png`、`81.png`、`89.png`：真实 OCR 误识别回归样本。
- `result_level4.png`：等级结果弹窗。
- `timeout_level3.png`：超时页面。

产物按样本名写入 `output\<sample>`，例如 `output\58`：

- `01_prompt_crop.png`：按脚本比例裁剪的题目区域。
- `02_warm_mask.png`：基于 RGB 通道差异的颜色掩码。
- `03_hsv_mask.png`：基于 HSV 色相、饱和度和值的掩码。
- `04_combined_closed_mask.png`：合并并经过形态学闭运算的掩码。
- `05_tesseract_input.png`：Tesseract 备用 OCR 的输入图。
- `results.txt`：RapidOCR 和各 PSM 模式的识别结果。

`results.txt` 会记录每个 PSM 的原始文本、解析数字和匹配情况。
`output` 目录已加入 `.gitignore`，产物只保留在本地，不提交到 Git。
