# OpenCV 预处理与 OCR 测试

使用 `input` 目录中的游戏截图，验证二进制速算题目的 OpenCV 预处理和 Tesseract OCR。

运行：

```powershell
.\.venv\Scripts\python.exe automation\tests\test_preprocess_ocr.py automation\tests\input\58.png --expected 58
.\.venv\Scripts\python.exe automation\tests\test_preprocess_ocr.py automation\tests\input\79.png --expected 79
```

产物按样本名写入 `output\<sample>`，例如 `output\58`：

- `01_prompt_crop.png`：按脚本比例裁剪的题目区域。
- `02_warm_mask.png`：基于 RGB 通道差异的颜色掩码。
- `03_hsv_mask.png`：基于 HSV 色相、饱和度和值的掩码。
- `04_combined_closed_mask.png`：合并并经过形态学闭运算的掩码。
- `05_tesseract_input.png`：最终交给 Tesseract 的输入图。
- `results.txt`：各 PSM 模式的识别结果。

`results.txt` 会记录每个 PSM 的原始文本、解析数字和匹配情况。
`output` 目录已加入 `.gitignore`，产物只保留在本地，不提交到 Git。
