"""
Mouse control utility for Claude
Move, click, drag, and scroll
"""
import pyautogui
import sys
import time

# Safety: set fail-safe (move mouse to top-left corner to abort)
pyautogui.FAILSAFE = True

def get_position():
    """Get current mouse position"""
    x, y = pyautogui.position()
    print(f"Mouse position: ({x}, {y})")
    return x, y

def move_to(x, y, duration=0.5):
    """Move mouse to absolute position"""
    print(f"Moving mouse to ({x}, {y})")
    pyautogui.moveTo(x, y, duration=duration)

def move_relative(x, y, duration=0.5):
    """Move mouse relative to current position"""
    print(f"Moving mouse by ({x}, {y})")
    pyautogui.move(x, y, duration=duration)

def click(x=None, y=None, button='left', clicks=1):
    """Click at position (or current position if None)"""
    if x is not None and y is not None:
        print(f"Clicking {button} button at ({x}, {y})")
        pyautogui.click(x, y, button=button, clicks=clicks)
    else:
        print(f"Clicking {button} button at current position")
        pyautogui.click(button=button, clicks=clicks)

def drag_to(x, y, duration=0.5, button='left'):
    """Drag from current position to target"""
    print(f"Dragging to ({x}, {y})")
    pyautogui.drag(x, y, duration=duration, button=button)

def scroll(amount, x=None, y=None):
    """Scroll (positive = up, negative = down)"""
    if x is not None and y is not None:
        pyautogui.moveTo(x, y)
    print(f"Scrolling by {amount}")
    pyautogui.scroll(amount)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  py mouse_control.py position")
        print("  py mouse_control.py move X Y [duration]")
        print("  py mouse_control.py click [X Y] [left|right|middle]")
        print("  py mouse_control.py doubleclick X Y")
        print("  py mouse_control.py drag X Y [duration]")
        print("  py mouse_control.py scroll AMOUNT [X Y]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "position":
        get_position()

    elif command == "move":
        x, y = int(sys.argv[2]), int(sys.argv[3])
        duration = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        move_to(x, y, duration)

    elif command == "click":
        if len(sys.argv) >= 4 and sys.argv[2].isdigit():
            x, y = int(sys.argv[2]), int(sys.argv[3])
            button = sys.argv[4] if len(sys.argv) > 4 else 'left'
            click(x, y, button=button)
        else:
            button = sys.argv[2] if len(sys.argv) > 2 else 'left'
            click(button=button)

    elif command == "doubleclick":
        x, y = int(sys.argv[2]), int(sys.argv[3])
        click(x, y, clicks=2)

    elif command == "drag":
        x, y = int(sys.argv[2]), int(sys.argv[3])
        duration = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        drag_to(x, y, duration)

    elif command == "scroll":
        amount = int(sys.argv[2])
        if len(sys.argv) >= 5:
            x, y = int(sys.argv[3]), int(sys.argv[4])
            scroll(amount, x, y)
        else:
            scroll(amount)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
