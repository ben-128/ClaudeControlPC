# Claude PC Control System

Complete automation system enabling Claude to control PC via mouse, keyboard, and OCR vision.

---

## 📋 QUICK SUMMARY FOR CLAUDE

**System Status:** ✅ OPERATIONAL

**What Works:**
- ✅ EasyOCR text detection with exact pixel coordinates (99%+ accuracy)
- ✅ **Advanced OpenCV UI detection** - color + shape + smart parsing
- ✅ Smart detection from natural descriptions ("green circular play button")
- ✅ Multi-color support (red, green, blue, yellow, orange, purple, cyan, etc.)
- ✅ Shape detection (circles, triangles, rectangles, polygons)
- ✅ Smooth mouse movement with configurable timing (0.5s lerp)
- ✅ Click delay for human-like behavior (0.25s wait before click)
- ✅ Keyboard control (text typing, key presses, hotkeys)
- ✅ Screenshot capture with single temp file reuse

## 🎯 MANDATORY 3-STEP WORKFLOW (ALWAYS FOLLOW)

### Step 1: Semantic Analysis (Claude Visual Understanding)
- **I** look at the screenshot myself
- Understand what's displayed on screen
- Identify the target element (button, text, icon, etc.)
- Understand the context and user intention
- Create natural language description (e.g., "green circular play button")
- **Output:** Description of what needs to be clicked

### Step 2: Hierarchical Detection (Automatic Fallback)
**Use `detect_unified.py` - tries methods in order:**

1. **GroundingDINO** (Priority #1)
   - Semantic understanding of UI elements
   - Best accuracy for complex descriptions
   - ~2-3s on CPU, ~700MB model

2. **EasyOCR** (Priority #2)
   - Text detection (99%+ accuracy)
   - Triggered if description contains text-like words
   - ~0.5s per detection

3. **OpenCV Advanced** (Fallback)
   - Color + shape detection
   - Fast (<0.1s), always available
   - Parses descriptions for color/shape hints

**Output:** Exact pixel coordinates [x, y] + method used

### Step 3: Action (Mouse Movement & Click)
- Move mouse to detected coordinates
- Smooth movement (0.5s lerp) + delay (0.25s)
- Execute click
- **Output:** Confirmation of action performed

**Critical Rules:**
- ❌ **NEVER skip Step 2** - Always use detection scripts
- ❌ **NEVER estimate coordinates** - VLM spatial reasoning is unreliable (300-350px errors)
- ✅ **ALWAYS detect, never guess** - Use OCR for text, OpenCV for icons
- ✅ **UTF-8 flag required** on Windows: `py -3 -X utf8`

**Key Lesson Learned:**
- Grid system + visual estimation = FAILED (300-350px errors)
- OCR + OpenCV detection = SUCCESS (pixel-perfect, zero estimation)

---

## 🚀 Installation

### 1. Install Python Packages
```bash
cd C:\Perso\Claude_ControlPc
pip install easyocr torch pillow opencv-python numpy pyautogui
```

### 2. First Run (One-Time Model Download)
```bash
py -3 -X utf8 easy_ocr_vision.py text temp_screen.png "test"
```
Downloads ~100MB of neural network models to `%USERPROFILE%\.EasyOCR\model\`

**⚠️ IMPORTANT:** Always use `-X utf8` flag on Windows to prevent encoding errors.

---

## 📖 Usage Guide

### OCR Text Detection

#### Find Text Coordinates
```bash
py -3 -X utf8 easy_ocr_vision.py text screenshot.png "Solo"
```

**Output:**
```json
{
  "found": true,
  "matches": [{
    "text": "Solo",
    "bbox": [566, 334, 612, 358],
    "center": [589, 346],
    "confidence": 0.995
  }]
}
```

#### Click Text Automatically (Smooth)
```bash
py -3 -X utf8 easy_ocr_vision.py click screenshot.png "Solo"
```
- Moves smoothly to center (0.5s lerp)
- Waits 0.25s before clicking
- Clicks left button

#### Find All Text (Debug)
```bash
py -3 -X utf8 easy_ocr_vision.py all screenshot.png 0.3
```
Returns JSON with all detected text + coordinates.

### Mouse Control

#### Smooth Click (with movement)
```bash
py -3 mouse_control.py click 800 400
```
- Default: 0.5s smooth movement + 0.25s delay before click
- Custom timing: `py -3 mouse_control.py click 800 400 left 0.3 0.1`

#### Move Mouse (no click)
```bash
py -3 mouse_control.py move 800 400 0.5
```
Smooth movement over 0.5 seconds.

#### Get Current Position
```bash
py -3 mouse_control.py position
```

#### Drag
```bash
py -3 mouse_control.py drag 1000 500 1.0
```
Smooth drag over 1 second.

#### Scroll
```bash
py -3 mouse_control.py scroll 5
```
Positive = up, negative = down.

### Keyboard Control

#### Type Text
```bash
py -3 keyboard_control.py type "Hello World"
```

#### Press Key
```bash
py -3 keyboard_control.py press space
py -3 keyboard_control.py press enter 3
```

#### Hotkey Combination
```bash
py -3 keyboard_control.py hotkey ctrl c
py -3 keyboard_control.py hotkey ctrl shift esc
```

### Screenshot Capture

```bash
py -3 claude_vision.py capture
```
Saves to `temp_screen.png` (auto-reuses same file for efficiency).

---

## 💡 Examples

### Unity Game Automation
```bash
# Capture current screen
py -3 claude_vision.py capture

# Click Play button with OCR
py -3 -X utf8 easy_ocr_vision.py click temp_screen.png "Play"

# Wait for game to load
timeout /t 2

# Press Space to start
py -3 keyboard_control.py press space

# Click Solo menu button
py -3 -X utf8 easy_ocr_vision.py click temp_screen.png "Solo"
```

### Custom Timing Example
```bash
# Very slow smooth click (2s movement, 0.5s delay)
py -3 mouse_control.py click 500 300 left 2.0 0.5

# Fast click (0.2s movement, 0.1s delay)
py -3 mouse_control.py click 500 300 left 0.2 0.1
```

---

## 🔧 Configuration

### Default Timings (Smooth & Natural)
- **Move duration:** 0.5s (lerp from current to target)
- **Click delay:** 0.25s (wait after arrival before clicking)

### Adjust in Code
**easy_ocr_vision.py:**
```python
def click_text(image_path, search_text, confidence=0.5,
               move_duration=0.5, click_delay=0.25):
```

**mouse_control.py:**
```python
def click(x=None, y=None, button='left', clicks=1,
          move_duration=0.5, click_delay=0.25):
```

### OCR Confidence Threshold
Default: 0.5 (50% confidence)

- **Blurry text:** Lower to 0.3
- **Clean text only:** Raise to 0.8

Example: `py -3 -X utf8 easy_ocr_vision.py text screenshot.png "Menu" 0.7`

---

## 🐛 Troubleshooting

### "charmap codec can't encode character"
**Symptom:** Unicode encoding error on Windows.

**Fix:** Add `-X utf8` flag:
```bash
py -3 -X utf8 easy_ocr_vision.py ...
```

### OCR Not Finding Text
1. **Check confidence** - Try lower threshold (0.3)
2. **Debug what's detected:**
   ```bash
   py -3 -X utf8 easy_ocr_vision.py all screenshot.png 0.1
   ```
3. **Text too small/blurry** - EasyOCR has resolution limits

### Mouse Clicking Wrong Location
**Don't manually estimate coordinates!** Use OCR:
- ❌ `py -3 mouse_control.py click 500 300` (estimated coords = fails)
- ✅ `py -3 -X utf8 easy_ocr_vision.py click temp_screen.png "Button"` (OCR = works)

### Slow First Run
Normal - downloading 100MB of neural network models. Subsequent runs are fast (models cached).

---

## 📚 Technical Details

### Why OCR-Based Detection?

**Previous failed approaches:**
1. **Grid System** - 300-350px errors (VLM spatial reasoning limitation)
2. **YOLO** - Detected "tv" instead of UI buttons (trained on real-world objects)
3. **Tesseract** - Download blocked (403 Forbidden)

**EasyOCR solution:**
- ✅ Pure Python (no external binaries)
- ✅ Neural network text detection
- ✅ Exact pixel coordinates (no estimation)
- ✅ 99%+ confidence on clear text
- ✅ Works reliably on UI elements

See `GRID_SYSTEM_FAILURE.md` for detailed failure analysis.

### Smooth Movement Implementation

PyAutoGUI's `moveTo()` uses **linear interpolation (lerp)**:
```python
pyautogui.moveTo(x, y, duration=0.5)
```
Calculates intermediate points between current and target position, moving smoothly over the duration.

**Click delay** adds human-like behavior:
```python
time.sleep(0.25)  # Wait after arrival before clicking
```

### File Structure
```
C:\Perso\Claude_ControlPc\
├── README.md                    # This file
├── EASYOCR_INSTALLATION.md      # Detailed installation guide
├── GRID_SYSTEM_FAILURE.md       # Why previous approaches failed
├── easy_ocr_vision.py           # OCR detection + clicking
├── mouse_control.py             # Smooth mouse control
├── keyboard_control.py          # Keyboard automation
├── claude_vision.py             # Screenshot capture
├── setup.py                     # Dependency checker
└── temp_screen.png              # Screenshot temp file (auto-reused)
```

### Models Location
- **Windows:** `C:\Users\<USERNAME>\.EasyOCR\model\`
- **Files:** `craft_mlt_25k.pth` (detection, ~50MB) + `english_g2.pth` (recognition, ~50MB)

---

## ⚠️ Critical Reminders

1. **NEVER estimate coordinates visually** - Use OCR instead
2. **Always use `-X utf8` flag** on Windows
3. **Smooth clicks are default** - 0.5s move + 0.25s delay
4. **OCR confidence default is 0.5** - Adjust for blurry/clean text
5. **First run downloads models** - ~100MB, one-time only

---

## ✅ Tested & Working

| Feature | Status | Notes |
|---------|--------|-------|
| EasyOCR text detection | ✅ Working | 99%+ confidence on clear text |
| Click with OCR | ✅ Working | Clicked "Solo" at (589, 346) successfully |
| Smooth mouse movement | ✅ Working | 0.5s lerp by default |
| Click delay | ✅ Working | 0.25s wait before click |
| Keyboard control | ✅ Working | Type, press, hotkeys all functional |
| Screenshot capture | ✅ Working | Auto-reuses temp_screen.png |
| UTF-8 encoding fix | ✅ Working | `-X utf8` flag prevents errors |

**Last tested:** 2026-02-13
**Test case:** Unity game "Solo" button - detected at (589, 346), clicked successfully
**Previous errors:** 300-350px with visual estimation (RESOLVED with OCR)

---

## 📖 See Also

- `EASYOCR_INSTALLATION.md` - Detailed installation instructions
- `GRID_SYSTEM_FAILURE.md` - Why visual estimation failed (important lesson)
- EasyOCR docs: https://github.com/JaidedAI/EasyOCR
- PyAutoGUI docs: https://pyautogui.readthedocs.io/
