"""
OCR-based UI Detection
Uses pytesseract to find text elements and their exact coordinates
NO visual estimation by Claude required
"""
import sys
import json
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

# Configure Tesseract path (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if Path(TESSERACT_PATH).exists():
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def find_text(image_path, search_text, confidence=60):
    """
    Find text on screen using OCR
    Returns exact coordinates of bounding boxes

    Args:
        image_path: Path to screenshot
        search_text: Text to find (e.g., "Solo", "Play")
        confidence: Minimum OCR confidence (0-100)

    Returns:
        List of matches with exact coordinates
    """
    if not HAS_OCR:
        return {"error": "pytesseract not installed", "found": False}

    try:
        img = Image.open(image_path)

        # Run OCR with bounding boxes
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

        matches = []
        for i, text in enumerate(data['text']):
            if search_text.lower() in text.lower():
                conf = int(data['conf'][i])
                if conf >= confidence:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                    matches.append({
                        "text": text,
                        "bbox": [x, y, x+w, y+h],
                        "center": [x + w//2, y + h//2],
                        "confidence": conf
                    })

        return {
            "found": len(matches) > 0,
            "count": len(matches),
            "matches": matches,
            "search": search_text
        }

    except Exception as e:
        return {"error": str(e), "found": False}

def find_all_text(image_path, min_confidence=60):
    """
    Extract ALL text from screen with positions
    Useful for debugging/exploration
    """
    if not HAS_OCR:
        return {"error": "pytesseract not installed"}

    try:
        img = Image.open(image_path)
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

        texts = []
        for i, text in enumerate(data['text']):
            if text.strip() and int(data['conf'][i]) >= min_confidence:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                texts.append({
                    "text": text,
                    "bbox": [x, y, x+w, y+h],
                    "center": [x + w//2, y + h//2],
                    "confidence": int(data['conf'][i])
                })

        return {
            "count": len(texts),
            "texts": texts
        }

    except Exception as e:
        return {"error": str(e)}

def find_rectangles(image_path, min_area=1000, max_area=100000):
    """
    Detect rectangular shapes (buttons) using OpenCV contours
    Returns coordinates without Claude estimation
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rectangles = []
        for contour in contours:
            # Approximate to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Filter rectangles (4 corners)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h

                if min_area <= area <= max_area:
                    rectangles.append({
                        "bbox": [x, y, x+w, y+h],
                        "center": [x + w//2, y + h//2],
                        "width": w,
                        "height": h,
                        "area": area
                    })

        # Sort by area (largest first)
        rectangles.sort(key=lambda r: r["area"], reverse=True)

        return {
            "found": len(rectangles) > 0,
            "count": len(rectangles),
            "rectangles": rectangles
        }

    except Exception as e:
        return {"error": str(e), "found": False}

def hybrid_detect(image_path, search_text, rect_filter=None):
    """
    Hybrid: OCR + rectangle detection
    Find text AND nearby rectangles (buttons containing text)
    """
    # Find text
    text_result = find_text(image_path, search_text)

    # Find rectangles
    rect_result = find_rectangles(image_path)

    if not text_result.get("found"):
        return {"found": False, "error": f"Text '{search_text}' not found"}

    # Match text with rectangles (find button containing text)
    text_match = text_result["matches"][0]
    text_center = text_match["center"]

    # Find rectangle containing this text
    for rect in rect_result.get("rectangles", []):
        bbox = rect["bbox"]
        if (bbox[0] <= text_center[0] <= bbox[2] and
            bbox[1] <= text_center[1] <= bbox[3]):
            return {
                "found": True,
                "type": "button",
                "text": text_match["text"],
                "bbox": bbox,
                "center": rect["center"],
                "confidence": text_match["confidence"]
            }

    # No rectangle found, use text bbox
    return {
        "found": True,
        "type": "text",
        "text": text_match["text"],
        "bbox": text_match["bbox"],
        "center": text_match["center"],
        "confidence": text_match["confidence"]
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "text": "py ocr_vision.py text IMAGE 'Search Text'",
                "all": "py ocr_vision.py all IMAGE [min_conf]",
                "rectangles": "py ocr_vision.py rectangles IMAGE",
                "hybrid": "py ocr_vision.py hybrid IMAGE 'Search Text'",
                "click": "py ocr_vision.py click IMAGE 'Text' (finds and clicks)"
            },
            "note": "Requires Tesseract OCR installed",
            "install": "https://github.com/UB-Mannheim/tesseract/wiki"
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "text":
        image = sys.argv[2]
        search = sys.argv[3]
        result = find_text(image, search)

    elif command == "all":
        image = sys.argv[2]
        min_conf = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        result = find_all_text(image, min_conf)

    elif command == "rectangles":
        image = sys.argv[2]
        result = find_rectangles(image)

    elif command == "hybrid":
        image = sys.argv[2]
        search = sys.argv[3]
        result = hybrid_detect(image, search)

    elif command == "click":
        image = sys.argv[2]
        search = sys.argv[3]
        result = hybrid_detect(image, search)

        if result.get("found"):
            import pyautogui
            x, y = result["center"]
            pyautogui.click(x, y)
            result["clicked"] = True
            result["clicked_at"] = {"x": x, "y": y}

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
