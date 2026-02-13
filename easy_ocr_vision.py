"""
EasyOCR-based UI Detection
Pure Python OCR - no external binaries required!
Finds text elements and returns exact coordinates automatically
"""
import sys
import json
import os

try:
    import easyocr
    import cv2
    import numpy as np
    from PIL import Image
    HAS_EASYOCR = True
except ImportError:
    HAS_EASYOCR = False

# Initialize EasyOCR reader (lazy loading)
_reader = None

def get_reader():
    """Lazy load EasyOCR reader"""
    global _reader
    if _reader is None:
        print("Initializing EasyOCR (first time only)...", file=sys.stderr)
        _reader = easyocr.Reader(['en'], gpu=False, verbose=False)  # English only, CPU mode, no progress bar
    return _reader

def find_text(image_path, search_text, confidence=0.5):
    """
    Find text on screen using EasyOCR
    Returns exact coordinates of bounding boxes

    Args:
        image_path: Path to screenshot
        search_text: Text to find (e.g., "Solo", "Play")
        confidence: Minimum OCR confidence (0.0-1.0)

    Returns:
        Dict with matches and exact coordinates
    """
    if not HAS_EASYOCR:
        return {"error": "easyocr not installed", "found": False}

    try:
        reader = get_reader()

        # Read text from image
        results = reader.readtext(image_path)

        matches = []
        for (bbox, text, conf) in results:
            if search_text.lower() in text.lower() and conf >= confidence:
                # bbox is [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                # Convert to [x1, y1, x2, y2] format
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]

                x1, x2 = int(min(x_coords)), int(max(x_coords))
                y1, y2 = int(min(y_coords)), int(max(y_coords))

                matches.append({
                    "text": text,
                    "bbox": [x1, y1, x2, y2],
                    "center": [(x1 + x2) // 2, (y1 + y2) // 2],
                    "confidence": round(conf, 3)
                })

        return {
            "found": len(matches) > 0,
            "count": len(matches),
            "matches": matches,
            "search": search_text
        }

    except Exception as e:
        return {"error": str(e), "found": False}

def find_all_text(image_path, min_confidence=0.5):
    """
    Extract ALL text from screen with positions
    Useful for debugging/exploration
    """
    if not HAS_EASYOCR:
        return {"error": "easyocr not installed"}

    try:
        reader = get_reader()
        results = reader.readtext(image_path)

        texts = []
        for (bbox, text, conf) in results:
            if conf >= min_confidence:
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]

                x1, x2 = int(min(x_coords)), int(max(x_coords))
                y1, y2 = int(min(y_coords)), int(max(y_coords))

                texts.append({
                    "text": text,
                    "bbox": [x1, y1, x2, y2],
                    "center": [(x1 + x2) // 2, (y1 + y2) // 2],
                    "confidence": round(conf, 3)
                })

        return {
            "count": len(texts),
            "texts": texts
        }

    except Exception as e:
        return {"error": str(e)}

def click_text(image_path, search_text, confidence=0.5, move_duration=0.5, click_delay=0.25):
    """
    Find text and click on it automatically
    No coordinate estimation needed!

    Args:
        image_path: Path to screenshot
        search_text: Text to find and click
        confidence: Minimum OCR confidence (0.0-1.0)
        move_duration: Time in seconds for smooth mouse movement (default 0.5s)
        click_delay: Delay in seconds between arrival and click (default 0.25s)
    """
    result = find_text(image_path, search_text, confidence)

    if result.get("found"):
        import pyautogui
        import time

        match = result["matches"][0]
        x, y = match["center"]

        # Smooth movement to destination (lerp)
        pyautogui.moveTo(x, y, duration=move_duration)

        # Wait before clicking (more human-like)
        time.sleep(click_delay)

        # Click
        pyautogui.click()

        result["clicked"] = True
        result["clicked_at"] = {"x": x, "y": y}

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "text": "py easy_ocr_vision.py text IMAGE 'Search Text' [conf]",
                "all": "py easy_ocr_vision.py all IMAGE [conf]",
                "click": "py easy_ocr_vision.py click IMAGE 'Text' [conf]"
            },
            "note": "Pure Python OCR - no external dependencies!",
            "first_run": "First run downloads OCR models (~100MB)"
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "text":
        image = sys.argv[2]
        search = sys.argv[3]
        conf = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        result = find_text(image, search, conf)

    elif command == "all":
        image = sys.argv[2]
        conf = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
        result = find_all_text(image, conf)

    elif command == "click":
        image = sys.argv[2]
        search = sys.argv[3]
        conf = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        result = click_text(image, search, conf)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
