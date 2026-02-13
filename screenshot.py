"""
Screenshot utility for Claude
Takes a screenshot and saves it to a file
"""
import pyautogui
import sys
from datetime import datetime

def take_screenshot(filename=None, region=None):
    """
    Take a screenshot

    Args:
        filename: Output filename (default: timestamp-based)
        region: Tuple (x, y, width, height) to capture specific region

    Returns:
        Path to saved screenshot
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

    if region:
        screenshot = pyautogui.screenshot(region=region)
    else:
        screenshot = pyautogui.screenshot()

    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")
    return filename

if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = "screenshot.png"

    # Optional: region capture
    # Example: py screenshot.py output.png 100 100 800 600
    if len(sys.argv) >= 6:
        region = (int(sys.argv[2]), int(sys.argv[3]),
                  int(sys.argv[4]), int(sys.argv[5]))
        take_screenshot(output_file, region)
    else:
        take_screenshot(output_file)
