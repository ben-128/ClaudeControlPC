"""
Unified UI Detection System
Hierarchical detection: GroundingDINO → EasyOCR → OpenCV
Uses best available method automatically
"""
import sys
import json
from pathlib import Path

# Import all detection methods
try:
    from detect_ui_grounding import detect_ui_elements as grounding_detect
    from detect_ui_grounding import HAS_GROUNDING_DINO
except:
    HAS_GROUNDING_DINO = False

try:
    from easy_ocr_vision import find_text as ocr_find
    HAS_EASYOCR = True
except:
    HAS_EASYOCR = False

try:
    from detect_ui_advanced import smart_detect as opencv_detect
    HAS_OPENCV = True
except:
    HAS_OPENCV = False

def unified_detect(image_path, description, target_y=None, y_tolerance=20, confidence=0.5):
    """
    Unified detection with automatic fallback

    Hierarchy:
    1. GroundingDINO (if available) - Best for UI elements
    2. EasyOCR (if text in description) - Best for text
    3. OpenCV Advanced (fallback) - Fast, always works

    Args:
        image_path: Path to screenshot
        description: Natural language description
        target_y: Optional Y coordinate filter
        y_tolerance: Y coordinate tolerance
        confidence: Minimum confidence threshold

    Returns:
        Dict with detection results + method used
    """
    results = {
        "description": description,
        "target_y": target_y,
        "methods_tried": [],
        "found": False
    }

    # Method 1: GroundingDINO (Priority #1)
    if HAS_GROUNDING_DINO:
        print("Trying GroundingDINO...", file=sys.stderr)
        results["methods_tried"].append("GroundingDINO")

        try:
            grounding_result = grounding_detect(
                image_path,
                description,
                box_threshold=0.30,
                text_threshold=0.20,
                target_y=target_y,
                y_tolerance=y_tolerance
            )

            if grounding_result.get("found"):
                # Convert to unified format
                detection = grounding_result["detections"][0]
                results["found"] = True
                results["method"] = "GroundingDINO"
                results["center"] = detection["center"]
                results["bbox"] = detection["bbox"]
                results["confidence"] = detection["confidence"]
                results["details"] = detection
                return results

        except Exception as e:
            print(f"GroundingDINO failed: {e}", file=sys.stderr)

    # Method 2: EasyOCR (Priority #2) - for text elements
    # Check if description seems to be looking for text
    desc_lower = description.lower()
    looks_like_text = any(word in desc_lower for word in ["text", "label", "title", "button with", "says", "word"])

    # Also try OCR if description contains specific words (potential button text)
    words = desc_lower.split()
    potential_text = [w for w in words if len(w) > 3 and w not in ["button", "green", "circular", "play", "icon", "red", "blue"]]

    if (looks_like_text or len(potential_text) > 0) and HAS_EASYOCR:
        print("Trying EasyOCR...", file=sys.stderr)
        results["methods_tried"].append("EasyOCR")

        try:
            # Try each potential text word
            for search_word in potential_text:
                ocr_result = ocr_find(image_path, search_word, confidence)

                if ocr_result.get("found"):
                    match = ocr_result["matches"][0]

                    # Filter by Y if specified
                    if target_y is not None:
                        if abs(match["center"][1] - target_y) > y_tolerance:
                            continue

                    results["found"] = True
                    results["method"] = "EasyOCR"
                    results["center"] = match["center"]
                    results["bbox"] = match["bbox"]
                    results["confidence"] = match["confidence"]
                    results["text"] = match["text"]
                    results["details"] = match
                    return results

        except Exception as e:
            print(f"EasyOCR failed: {e}", file=sys.stderr)

    # Method 3: OpenCV Advanced (Last Resort)
    if HAS_OPENCV:
        print("Trying OpenCV Advanced...", file=sys.stderr)
        results["methods_tried"].append("OpenCV Advanced")

        try:
            opencv_result = opencv_detect(
                image_path,
                description,
                target_y=target_y,
                tolerance=y_tolerance
            )

            if opencv_result.get("found"):
                match = opencv_result["matches"][0]
                results["found"] = True
                results["method"] = "OpenCV Advanced"
                results["center"] = match["center"]
                results["bbox"] = match["bbox"]
                results["color"] = match.get("color")
                results["shape"] = match.get("shape")
                results["details"] = match
                return results

        except Exception as e:
            print(f"OpenCV Advanced failed: {e}", file=sys.stderr)

    # Nothing found
    results["error"] = "No detection method succeeded"
    return results

def click_unified(image_path, description, target_y=None, y_tolerance=20, confidence=0.5):
    """
    Detect and return click coordinates using unified detection

    Args:
        image_path: Path to screenshot
        description: Natural description of element to click
        target_y: Optional Y filter
        y_tolerance: Y tolerance
        confidence: Minimum confidence

    Returns:
        Dict with detection + click coordinates
    """
    result = unified_detect(image_path, description, target_y, y_tolerance, confidence)

    if result["found"]:
        result["should_click"] = True
        result["click_at"] = result["center"]
    else:
        result["should_click"] = False

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "detect": "py detect_unified.py detect IMAGE 'description' [target_y] [tolerance] [conf]",
                "click": "py detect_unified.py click IMAGE 'description' [target_y] [tolerance] [conf]"
            },
            "examples": {
                "detect": "py detect_unified.py detect temp.png 'green play button' 556 15",
                "click": "py detect_unified.py click temp.png 'Solo button' 0.5"
            },
            "hierarchy": [
                "1. GroundingDINO (semantic understanding, best accuracy)",
                "2. EasyOCR (text detection, 99% accuracy)",
                "3. OpenCV Advanced (color+shape, fast fallback)"
            ],
            "available": {
                "GroundingDINO": HAS_GROUNDING_DINO,
                "EasyOCR": HAS_EASYOCR,
                "OpenCV": HAS_OPENCV
            }
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "detect":
        image = sys.argv[2]
        description = sys.argv[3]
        target_y = int(sys.argv[4]) if len(sys.argv) > 4 else None
        tolerance = int(sys.argv[5]) if len(sys.argv) > 5 else 20
        conf = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5
        result = unified_detect(image, description, target_y, tolerance, conf)

    elif command == "click":
        image = sys.argv[2]
        description = sys.argv[3]
        target_y = int(sys.argv[4]) if len(sys.argv) > 4 else None
        tolerance = int(sys.argv[5]) if len(sys.argv) > 5 else 20
        conf = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5
        result = click_unified(image, description, target_y, tolerance, conf)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
