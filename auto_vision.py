"""
Auto Vision System - NO REFERENCE IMAGES NEEDED
Uses OCR, color detection, and heuristics to find UI elements
"""
import pyautogui
import cv2
import numpy as np
import sys
import json
from pathlib import Path

# Try to import pytesseract (optional)
try:
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

def screenshot_to_cv2():
    """Take screenshot and convert to OpenCV format (in memory)"""
    screenshot = pyautogui.screenshot()
    # Convert PIL to numpy array (OpenCV format)
    img_np = np.array(screenshot)
    # Convert RGB to BGR (OpenCV format)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return img_bgr

def find_text_ocr(text, confidence=0.6):
    """
    Find text on screen using OCR
    Returns: List of positions where text was found
    """
    if not HAS_OCR:
        return {"error": "Tesseract not installed", "found": False}

    try:
        screenshot = pyautogui.screenshot()

        # Run OCR with bounding boxes
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

        results = []
        for i, word in enumerate(data['text']):
            if text.lower() in word.lower():
                conf = float(data['conf'][i]) / 100
                if conf >= confidence:
                    x = data['left'][i] + data['width'][i] // 2
                    y = data['top'][i] + data['height'][i] // 2

                    results.append({
                        "x": x,
                        "y": y,
                        "text": word,
                        "confidence": conf
                    })

        return {
            "found": len(results) > 0,
            "count": len(results),
            "locations": results
        }

    except Exception as e:
        return {"error": str(e), "found": False}

def find_buttons_by_color(color_range="green", min_size=20):
    """
    Find buttons by color detection (works for Unity Play button, etc.)
    color_range: "green", "blue", "red", or custom HSV range
    """
    img = screenshot_to_cv2()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color ranges
    color_ranges = {
        "green": ([40, 40, 40], [80, 255, 255]),     # Unity Play button (greenish)
        "blue": ([100, 40, 40], [130, 255, 255]),    # Blue buttons
        "red": ([0, 40, 40], [10, 255, 255]),        # Red buttons
        "dark": ([0, 0, 0], [180, 255, 80]),         # Dark buttons
        "light": ([0, 0, 200], [180, 30, 255]),      # Light buttons
    }

    if color_range in color_ranges:
        lower, upper = color_ranges[color_range]
    else:
        return {"error": f"Unknown color: {color_range}", "found": False}

    # Create mask
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    results = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_size * min_size:
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Calculate center
            center_x = x + w // 2
            center_y = y + h // 2

            results.append({
                "x": center_x,
                "y": center_y,
                "width": w,
                "height": h,
                "area": int(area)
            })

    # Sort by area (largest first)
    results.sort(key=lambda r: r["area"], reverse=True)

    return {
        "found": len(results) > 0,
        "count": len(results),
        "locations": results
    }

def find_unity_play_button():
    """
    Unity-specific heuristic: Play button is always center-top
    Combines color detection + position heuristic
    """
    # Unity Play button is typically:
    # - In the top center area (y < 100)
    # - Greenish color when inactive, blueish when active
    # - Around 30-40px wide

    results_green = find_buttons_by_color("green", min_size=15)
    results_blue = find_buttons_by_color("blue", min_size=15)

    # Combine results
    all_buttons = []
    if results_green.get("found"):
        all_buttons.extend(results_green["locations"])
    if results_blue.get("found"):
        all_buttons.extend(results_blue["locations"])

    # Filter for top-center buttons
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2

    top_center_buttons = [
        btn for btn in all_buttons
        if btn["y"] < 100 and abs(btn["x"] - center_x) < 300
    ]

    # Sort by proximity to center
    top_center_buttons.sort(key=lambda b: abs(b["x"] - center_x))

    if top_center_buttons:
        best = top_center_buttons[0]
        return {
            "found": True,
            "x": best["x"],
            "y": best["y"],
            "method": "unity_heuristic",
            "all_candidates": len(top_center_buttons)
        }
    else:
        return {"found": False, "error": "No Unity Play button found"}

def find_rectangles(min_width=50, min_height=30, max_width=300, max_height=100):
    """
    Find rectangular UI elements (buttons, panels, etc.)
    """
    img = screenshot_to_cv2()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    results = []
    for contour in contours:
        # Approximate contour to polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if it's approximately rectangular (4 corners)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)

            # Filter by size
            if (min_width <= w <= max_width and
                min_height <= h <= max_height):

                center_x = x + w // 2
                center_y = y + h // 2

                results.append({
                    "x": center_x,
                    "y": center_y,
                    "width": w,
                    "height": h
                })

    return {
        "found": len(results) > 0,
        "count": len(results),
        "locations": results
    }

def smart_click(target, method="auto"):
    """
    Intelligently find and click on a target
    target: text to find OR color name OR "unity_play"
    method: "ocr", "color", "unity", "rectangles", or "auto"
    """
    result = None

    if method == "auto":
        # Try multiple methods
        if target.lower() == "unity_play" or target.lower() == "play":
            result = find_unity_play_button()
        elif HAS_OCR:
            result = find_text_ocr(target)
        else:
            # Try color detection with common colors
            for color in ["green", "blue", "red"]:
                result = find_buttons_by_color(color)
                if result.get("found"):
                    break

    elif method == "ocr":
        result = find_text_ocr(target)

    elif method == "color":
        result = find_buttons_by_color(target)

    elif method == "unity":
        result = find_unity_play_button()

    elif method == "rectangles":
        result = find_rectangles()

    # Click if found
    if result and result.get("found"):
        locations = result.get("locations", [result])
        if locations:
            # Click first result
            first = locations[0]
            x, y = first.get("x"), first.get("y")
            if x is not None and y is not None:
                pyautogui.click(x, y)
                result["clicked"] = True
                result["clicked_at"] = {"x": x, "y": y}

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: py auto_vision.py <command> [args]",
            "ocr_available": HAS_OCR,
            "tesseract_note": "Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki if OCR needed",
            "commands": {
                "text": "py auto_vision.py text 'Play' [confidence]",
                "color": "py auto_vision.py color green|blue|red [min_size]",
                "unity": "py auto_vision.py unity",
                "rectangles": "py auto_vision.py rectangles [min_w] [min_h] [max_w] [max_h]",
                "click": "py auto_vision.py click <target> [method]"
            }
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "text":
        text = sys.argv[2]
        confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
        result = find_text_ocr(text, confidence)

    elif command == "color":
        color = sys.argv[2] if len(sys.argv) > 2 else "green"
        min_size = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        result = find_buttons_by_color(color, min_size)

    elif command == "unity":
        result = find_unity_play_button()

    elif command == "rectangles":
        min_w = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        min_h = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        max_w = int(sys.argv[4]) if len(sys.argv) > 4 else 300
        max_h = int(sys.argv[5]) if len(sys.argv) > 5 else 100
        result = find_rectangles(min_w, min_h, max_w, max_h)

    elif command == "click":
        target = sys.argv[2]
        method = sys.argv[3] if len(sys.argv) > 3 else "auto"
        result = smart_click(target, method)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
