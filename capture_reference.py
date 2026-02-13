"""
Interactive tool to capture reference images for smart_vision
Click on UI elements to save them as reference images
"""
import pyautogui
import sys
from pathlib import Path

def capture_region_interactive(output_name):
    """
    Interactive region capture:
    1. Shows current mouse position
    2. User clicks top-left corner
    3. User clicks bottom-right corner
    4. Saves region as reference image
    """
    print(f"=== Capturing Reference: {output_name} ===")
    print("Move mouse to TOP-LEFT corner of element and press ENTER...")

    input()
    x1, y1 = pyautogui.position()
    print(f"Top-left: ({x1}, {y1})")

    print("Move mouse to BOTTOM-RIGHT corner of element and press ENTER...")
    input()
    x2, y2 = pyautogui.position()
    print(f"Bottom-right: ({x2}, {y2})")

    # Calculate region
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    print(f"Capturing region: ({left}, {top}) {width}x{height}")

    # Capture and save
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # Save to references folder
    ref_dir = Path("references")
    ref_dir.mkdir(exist_ok=True)

    filepath = ref_dir / f"{output_name}.png"
    screenshot.save(filepath)

    print(f"Saved: {filepath}")
    print(f"Usage: py smart_vision.py find references/{output_name}.png")

    return str(filepath)

def quick_capture(output_name, size=50):
    """
    Quick capture: captures a square around current mouse position
    """
    print(f"=== Quick Capture: {output_name} ===")
    print(f"Move mouse to CENTER of element and press ENTER...")

    input()
    x, y = pyautogui.position()

    # Capture square region around mouse
    left = x - size // 2
    top = y - size // 2

    screenshot = pyautogui.screenshot(region=(left, top, size, size))

    ref_dir = Path("references")
    ref_dir.mkdir(exist_ok=True)

    filepath = ref_dir / f"{output_name}.png"
    screenshot.save(filepath)

    print(f"Saved: {filepath} ({size}x{size})")
    print(f"Usage: py smart_vision.py find references/{output_name}.png")

    return str(filepath)

if __name__ == "__main__":
    print("=== Reference Image Capture Tool ===")

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  py capture_reference.py <name> [mode] [size]")
        print("\nModes:")
        print("  interactive - Click top-left and bottom-right corners (default)")
        print("  quick - Captures square around mouse (specify size)")
        print("\nExamples:")
        print("  py capture_reference.py unity_play")
        print("  py capture_reference.py menu_button quick 80")
        sys.exit(1)

    name = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "interactive"

    if mode == "quick":
        size = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        quick_capture(name, size)
    else:
        capture_region_interactive(name)

    print("\nDone!")
