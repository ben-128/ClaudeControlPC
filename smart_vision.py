"""
Smart Vision System - Process screenshots in memory, return text results
No disk I/O except for reference images
"""
import pyautogui
import sys
import json
from pathlib import Path

def find_and_click(reference_image, confidence=0.8, click=True):
    """
    Find an image on screen and optionally click it
    Returns: JSON with status, position, or error
    """
    try:
        # Search in memory (no screenshot file created)
        location = pyautogui.locateOnScreen(reference_image, confidence=confidence)

        if location:
            center = pyautogui.center(location)
            result = {
                "found": True,
                "x": center.x,
                "y": center.y,
                "region": {
                    "left": location.left,
                    "top": location.top,
                    "width": location.width,
                    "height": location.height
                }
            }

            if click:
                pyautogui.click(center)
                result["clicked"] = True

            return result
        else:
            return {"found": False, "error": "Element not found on screen"}

    except Exception as e:
        return {"found": False, "error": str(e)}

def find_all(reference_image, confidence=0.8):
    """
    Find all instances of an image on screen
    Returns: JSON with all positions
    """
    try:
        locations = list(pyautogui.locateAllOnScreen(reference_image, confidence=confidence))

        results = []
        for loc in locations:
            center = pyautogui.center(loc)
            results.append({
                "x": center.x,
                "y": center.y,
                "region": {
                    "left": loc.left,
                    "top": loc.top,
                    "width": loc.width,
                    "height": loc.height
                }
            })

        return {
            "found": len(results) > 0,
            "count": len(results),
            "locations": results
        }

    except Exception as e:
        return {"found": False, "error": str(e)}

def analyze_region(x, y, width, height):
    """
    Analyze a specific screen region (in memory)
    Returns: JSON with pixel colors and basic info
    """
    try:
        # Capture region in memory
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Get dominant colors (sample center)
        center_pixel = screenshot.getpixel((width//2, height//2))

        result = {
            "region": {"x": x, "y": y, "width": width, "height": height},
            "center_color": {"r": center_pixel[0], "g": center_pixel[1], "b": center_pixel[2]},
            "size": {"width": screenshot.width, "height": screenshot.height}
        }

        return result

    except Exception as e:
        return {"error": str(e)}

def get_screen_info():
    """
    Get current screen state (mouse position, screen size, etc.)
    """
    try:
        width, height = pyautogui.size()
        x, y = pyautogui.position()

        return {
            "screen": {"width": width, "height": height},
            "mouse": {"x": x, "y": y},
            "pixel_at_mouse": pyautogui.pixel(x, y)
        }

    except Exception as e:
        return {"error": str(e)}

def wait_for_element(reference_image, timeout=10, confidence=0.8):
    """
    Wait for an element to appear on screen
    Returns: JSON with result when found or timeout
    """
    import time

    start_time = time.time()

    while time.time() - start_time < timeout:
        result = find_and_click(reference_image, confidence=confidence, click=False)

        if result.get("found"):
            result["wait_time"] = time.time() - start_time
            return result

        time.sleep(0.5)

    return {
        "found": False,
        "error": f"Timeout after {timeout}s",
        "wait_time": timeout
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: py smart_vision.py <command> [args]",
            "commands": {
                "find": "py smart_vision.py find <image> [confidence] [click_yes/no]",
                "findall": "py smart_vision.py findall <image> [confidence]",
                "region": "py smart_vision.py region <x> <y> <width> <height>",
                "info": "py smart_vision.py info",
                "wait": "py smart_vision.py wait <image> [timeout] [confidence]"
            }
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "find":
        image = sys.argv[2]
        confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
        click = sys.argv[4].lower() != "no" if len(sys.argv) > 4 else True
        result = find_and_click(image, confidence, click)

    elif command == "findall":
        image = sys.argv[2]
        confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
        result = find_all(image, confidence)

    elif command == "region":
        x, y, w, h = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        result = analyze_region(x, y, w, h)

    elif command == "info":
        result = get_screen_info()

    elif command == "wait":
        image = sys.argv[2]
        timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 10
        confidence = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8
        result = wait_for_element(image, timeout, confidence)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
