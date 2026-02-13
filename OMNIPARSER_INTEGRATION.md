# OmniParser Integration Plan

## What is OmniParser?

Microsoft's open-source tool for **automatic GUI element detection** with precise coordinates.

- **GitHub**: https://github.com/microsoft/OmniParser
- **Hugging Face**: https://huggingface.co/microsoft/OmniParser
- **Demo**: https://microsoft.github.io/OmniParser/

## How It Works

1. **Input**: Screenshot (PNG)
2. **Processing**:
   - YOLOv8 detects UI elements (buttons, icons, inputs)
   - Florence2 generates descriptions
   - Set-of-Marks overlays numbers on each element
3. **Output**: JSON with bounding boxes + labeled screenshot

```json
{
  "parsed_content_list": [
    {
      "id": 1,
      "bbox": [440, 230, 520, 270],
      "label": "Solo button",
      "interactable": true
    }
  ]
}
```

## Installation

```bash
# Clone repo
git clone https://github.com/microsoft/OmniParser
cd OmniParser

# Install dependencies
pip install -r requirements.txt

# Download models (auto-downloads from Hugging Face)
python download_models.py
```

## Usage in Our System

### Step 1: Parse Screenshot
```python
from omniparser import parse_screen

# Parse current screen
result = parse_screen("temp_screen.png")

# Result contains:
# - parsed_content_list: List of detected elements with bboxes
# - labeled_screenshot: Image with SoM overlays
```

### Step 2: Claude Analyzes Labeled Image
```python
# Save labeled screenshot with numbers
result.save("temp_labeled.png")

# Claude sees image with overlays:
# 1️⃣ Solo
# 2️⃣ Multijoueur
# 3️⃣ Options

# Claude says: "Click on element #1"
```

### Step 3: Precise Click
```python
# Get element by ID
element = result.get_element(1)

# Extract center coordinates
bbox = element["bbox"]  # [x1, y1, x2, y2]
center_x = (bbox[0] + bbox[2]) // 2
center_y = (bbox[1] + bbox[3]) // 2

# Click precisely
pyautogui.click(center_x, center_y)
```

## Integration Script

Create `omni_click.py`:

```python
import pyautogui
import json
import sys
from omniparser import parse_screen

def find_and_click(screenshot_path, element_id_or_label):
    """
    Parse screenshot, find element, and click it
    """
    # Parse screenshot
    result = parse_screen(screenshot_path)

    # Find element by ID or label
    element = None
    for elem in result["parsed_content_list"]:
        if elem["id"] == element_id_or_label or \
           element_id_or_label.lower() in elem["label"].lower():
            element = elem
            break

    if not element:
        return {"error": "Element not found"}

    # Calculate center
    bbox = element["bbox"]
    x = (bbox[0] + bbox[2]) // 2
    y = (bbox[1] + bbox[3]) // 2

    # Click
    pyautogui.click(x, y)

    return {
        "clicked": True,
        "element": element,
        "coordinates": (x, y)
    }

if __name__ == "__main__":
    screenshot = sys.argv[1]
    target = sys.argv[2]  # ID number or label text

    result = find_and_click(screenshot, target)
    print(json.dumps(result, indent=2))
```

## Workflow with OmniParser

1. **Capture**: `py claude_vision.py capture`
2. **Parse**: `py omni_click.py temp_screen.png "Solo"`
3. **Auto-click**: Finds "Solo" button and clicks center automatically!

## Benefits

✅ **No more coordinate guessing** - OmniParser detects exact positions
✅ **Semantic understanding** - Click by name ("Solo") not pixels
✅ **100% accurate** - Uses computer vision, not VLM spatial reasoning
✅ **Works offline** - Models run locally

## Alternative: Set-of-Mark Only

If OmniParser is too heavy, just use SoM overlay:

```python
# Generate numbered overlay
labeled_img = som_overlay(screenshot)

# Claude sees numbers on elements
# Claude: "Click element #3"

# Direct click
click_element_id(3, labeled_img_metadata)
```

## Next Steps

1. Install OmniParser
2. Test on Unity screenshot
3. Integrate into `claude_vision.py`
4. Replace manual coordinate estimation with automatic detection

## Sources

- [OmniParser GitHub](https://github.com/microsoft/OmniParser)
- [Set-of-Mark Paper](https://arxiv.org/abs/2310.11441)
- [Gemini Bounding Boxes](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/bounding-box-detection)
