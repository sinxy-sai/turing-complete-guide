# OpenCV 预处理测试

使用 `input_58.png` 验证二进制速算题目数字的预处理流程。

运行：

```powershell
.\.venv\Scripts\python.exe automation\tests\test_preprocess_58.py
```

产物位于 `output_58`：

- `01_prompt_crop.png`：按脚本比例裁剪的题目区域。
- `02_warm_mask.png`：基于 RGB 通道差异的颜色掩码。
- `03_hsv_mask.png`：基于 HSV 色相、饱和度和值的掩码。
- `04_combined_closed_mask.png`：合并并经过形态学闭运算的掩码。
- `05_tesseract_input.png`：最终交给 Tesseract 的输入图。
- `results.txt`：各 PSM 模式的识别结果。

当前截图的期望数字为 `58`，三个 PSM 模式均识别为 `58`。
