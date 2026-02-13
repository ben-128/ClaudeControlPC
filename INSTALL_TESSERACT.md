# Installing Tesseract OCR for Windows

## Download Tesseract

**Official Windows installer:**
https://github.com/UB-Mannheim/tesseract/wiki

**Direct download (recommended):**
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.5.1.exe

## Installation Steps

1. **Download** `tesseract-ocr-w64-setup-5.5.1.exe` (~75MB)

2. **Run installer**
   - Default path: `C:\Program Files\Tesseract-OCR`
   - ✅ Check "Add to PATH" (recommended)

3. **Verify installation**
   ```bash
   tesseract --version
   ```

## Quick Test

```bash
# Test OCR on screenshot
py ocr_vision.py all temp_screen.png

# Find "Solo" button
py ocr_vision.py text temp_screen.png "Solo"

# Click on "Solo" automatically
py ocr_vision.py click temp_screen.png "Solo"
```

## Alternative: Portable

If you can't install system-wide:

1. Download portable: https://digi.bib.uni-mannheim.de/tesseract/
2. Extract to `C:\Tesseract`
3. Update `ocr_vision.py` line 14:
   ```python
   TESSERACT_PATH = r"C:\Tesseract\tesseract.exe"
   ```

## How It Works

**OCR-based detection = NO Claude estimation needed!**

```
Screenshot → Tesseract OCR → Finds "Solo" text
                           → Returns bbox [x1,y1,x2,y2]
                           → Calculates center [(x1+x2)/2, (y1+y2)/2]
                           → Clicks EXACT center
```

**100% automated coordinates - no guessing!**
