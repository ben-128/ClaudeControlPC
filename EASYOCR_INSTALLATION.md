# EasyOCR Installation Guide

## What is EasyOCR?
EasyOCR is a pure Python OCR (Optical Character Recognition) library that:
- Detects text in screenshots automatically
- Returns exact pixel coordinates (no estimation needed)
- Works entirely in Python (no external binaries required)
- Downloads pre-trained neural network models on first use

## Why EasyOCR?
Previous approaches failed due to VLM spatial reasoning limitations (300-350px errors):
- **Grid system**: Required Claude to visually estimate grid cells → failed
- **YOLO**: Generic object detection trained on real-world objects (not UI) → detected "tv" instead of buttons
- **Tesseract**: Download blocked (403 Forbidden) → couldn't install

EasyOCR solves this by doing direct computer vision on screenshot pixels.

## Installation Steps

### 1. Install Python Packages
```bash
cd C:\Perso\Claude_ControlPc
pip install easyocr torch pillow opencv-python numpy pyautogui
```

**Packages installed:**
- `easyocr` - Main OCR library
- `torch` - PyTorch deep learning framework (EasyOCR backend)
- `pillow` - Image processing
- `opencv-python` - Computer vision utilities
- `numpy` - Numerical operations
- `pyautogui` - Mouse/keyboard control (already installed)

**Total size:** ~500-600MB (includes PyTorch)

### 2. First Run - Model Download
When you first run EasyOCR, it automatically downloads trained neural network models:

```bash
py -3 -X utf8 easy_ocr_vision.py text screenshot.png "Solo"
```

**What gets downloaded:**
- Detection model: ~50MB (CRAFT text detector)
- Recognition model: ~50MB (English character recognizer)
- **Downloaded to:** `%USERPROFILE%\.EasyOCR\model\`
- **One-time only** - subsequent runs use cached models

### 3. UTF-8 Encoding (Windows Only)
**CRITICAL**: Always run Python with `-X utf8` flag on Windows:
```bash
py -3 -X utf8 easy_ocr_vision.py ...
```

**Why?** EasyOCR's progress bar uses Unicode block characters (`█`). Without UTF-8:
- Error: `'charmap' codec can't encode character '\u2588'`
- Download fails or OCR doesn't run

**Alternative**: Edit `easy_ocr_vision.py` to set `verbose=False` (already done)

## Usage Examples

### Find Text Coordinates
```bash
py -3 -X utf8 easy_ocr_vision.py text temp_screen.png "Solo"
```

**Output:**
```json
{
  "found": true,
  "count": 1,
  "matches": [
    {
      "text": "Solo",
      "bbox": [566, 334, 612, 358],
      "center": [589, 346],
      "confidence": 0.995
    }
  ],
  "search": "Solo"
}
```

### Click Text Automatically
```bash
py -3 -X utf8 easy_ocr_vision.py click temp_screen.png "Solo"
```

**What happens:**
1. Captures screenshot
2. Detects all text regions
3. Finds "Solo" with OCR
4. Clicks center coordinates (589, 346)
5. Returns confirmation with clicked coordinates

### Extract All Text (Debug)
```bash
py -3 -X utf8 easy_ocr_vision.py all temp_screen.png 0.3
```

**Output:** JSON with all detected text + coordinates (useful for exploring what text is visible)

## Confidence Threshold
Default: 0.5 (50% confidence)

Adjust for:
- **Blurry text**: Lower to 0.3
- **Clean text only**: Raise to 0.8

Example:
```bash
py -3 -X utf8 easy_ocr_vision.py text screenshot.png "Menu" 0.7
```

## Model Storage Location
- **Windows:** `C:\Users\<USERNAME>\.EasyOCR\model\`
- **Linux/Mac:** `~/.EasyOCR/model/`

**Files:**
- `craft_mlt_25k.pth` - Text detection model (~50MB)
- `english_g2.pth` - English recognition model (~50MB)

## Troubleshooting

### Progress bar encoding error
**Symptom:** `'charmap' codec can't encode character '\u2588'`

**Fix:** Add `-X utf8` flag:
```bash
py -3 -X utf8 easy_ocr_vision.py ...
```

### Slow first run
**Normal:** First run downloads 100MB of models. Subsequent runs are fast (models cached).

### "No text found" with text visible
**Causes:**
1. Confidence too high (try 0.3 instead of 0.5)
2. Text too small/blurry (EasyOCR has resolution limits)
3. Non-English text (need different language model)

**Debug:**
```bash
py -3 -X utf8 easy_ocr_vision.py all screenshot.png 0.1
```
Shows all detected text with confidence scores.

### PyTorch warnings
**Symptom:** `'pin_memory' argument is set as true but no accelerator is found`

**Explanation:** EasyOCR uses CPU mode (no GPU). Warning is harmless.

**Silence warnings:** Add to script:
```python
import warnings
warnings.filterwarnings('ignore')
```

## Performance

### CPU Mode (Current)
- First run: ~5-10 seconds (detection + recognition)
- Subsequent: ~3-5 seconds per screenshot
- Memory: ~500MB RAM

### GPU Mode (Optional)
Install CUDA + GPU-enabled PyTorch for ~10x speed:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

Then edit `easy_ocr_vision.py`:
```python
_reader = easyocr.Reader(['en'], gpu=True)  # Enable GPU
```

## Integration with Claude Code Automation

### Complete Workflow
1. **Capture screenshot:**
   ```python
   import pyautogui
   pyautogui.screenshot().save("temp_screen.png")
   ```

2. **Find text with EasyOCR:**
   ```bash
   py -3 -X utf8 easy_ocr_vision.py click temp_screen.png "Play"
   ```

3. **No coordinate estimation by Claude** - EasyOCR returns exact pixels automatically!

### Example: Unity Automation
```bash
# Click Play button
py -3 -X utf8 easy_ocr_vision.py click temp_screen.png "Play"

# Wait for game to load
timeout /t 2

# Press Space
py -3 mouse_control.py press space

# Click Solo menu button
py -3 -X utf8 easy_ocr_vision.py click temp_screen.png "Solo"
```

## Summary

✅ **Installed:** EasyOCR + PyTorch + dependencies
✅ **Models:** Auto-downloaded to `%USERPROFILE%\.EasyOCR\`
✅ **Working:** Detected "Solo" at (589, 346) with 99.5% confidence
✅ **Clicked:** Successfully clicked exact coordinates
✅ **Zero estimation errors** - OCR provides pixel-perfect coordinates

**Previous approaches:**
- Grid system: ❌ 300-350px errors (VLM spatial reasoning limitation)
- YOLO: ❌ Detected wrong objects ("tv" instead of UI)
- Tesseract: ❌ Download blocked

**EasyOCR solution:**
- ✅ Pure Python (no external binaries)
- ✅ Automatic model download
- ✅ Exact coordinate detection
- ✅ 99%+ confidence on clear text
- ✅ Works on UI elements reliably
