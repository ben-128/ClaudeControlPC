"""
Claude Vision System
Takes screenshot, saves to temp file for Claude to analyze visually
Claude provides exact coordinates, script clicks
"""
import pyautogui
import sys
import json

TEMP_FILE = "temp_screen.png"

def capture_for_claude():
    """Capture screen to temp file for Claude to analyze"""
    screenshot = pyautogui.screenshot()
    screenshot.save(TEMP_FILE)

    # Return screen dimensions for reference
    return {
        "status": "captured",
        "file": TEMP_FILE,
        "screen": {
            "width": screenshot.width,
            "height": screenshot.height
        }
    }

def click_at(x, y, duration=0.5):
    """Click at coordinates provided by Claude"""
    pyautogui.click(x, y, duration=duration)
    return {
        "status": "clicked",
        "x": x,
        "y": y
    }

def move_to(x, y, duration=0.5):
    """Move mouse to coordinates provided by Claude"""
    pyautogui.moveTo(x, y, duration=duration)
    return {
        "status": "moved",
        "x": x,
        "y": y
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "capture": "py claude_vision.py capture",
                "click": "py claude_vision.py click X Y [duration]",
                "move": "py claude_vision.py move X Y [duration]"
            }
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "capture":
        result = capture_for_claude()

    elif command == "click":
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        duration = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        result = click_at(x, y, duration)

    elif command == "move":
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        duration = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        result = move_to(x, y, duration)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
