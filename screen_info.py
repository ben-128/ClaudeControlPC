"""
Screen information utility
Get screen size, find images, locate UI elements
"""
import pyautogui
import sys

def get_screen_size():
    """Get screen dimensions"""
    width, height = pyautogui.size()
    print(f"Screen size: {width}x{height}")
    return width, height

def find_on_screen(image_path, confidence=0.9):
    """
    Find an image on screen
    Returns (x, y) of center if found, None otherwise
    """
    print(f"Looking for: {image_path}")
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            print(f"Found at: ({center.x}, {center.y})")
            print(f"Region: {location}")
            return center.x, center.y
        else:
            print("Not found on screen")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def find_all_on_screen(image_path, confidence=0.9):
    """Find all instances of an image on screen"""
    print(f"Looking for all instances of: {image_path}")
    try:
        locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
        print(f"Found {len(locations)} instance(s)")
        for i, loc in enumerate(locations):
            center = pyautogui.center(loc)
            print(f"  [{i}] Center: ({center.x}, {center.y}), Region: {loc}")
        return locations
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_pixel_color(x, y):
    """Get RGB color of pixel at position"""
    pixel = pyautogui.pixel(x, y)
    print(f"Pixel at ({x}, {y}): RGB{pixel}")
    return pixel

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  py screen_info.py size")
        print("  py screen_info.py find IMAGE_PATH [confidence]")
        print("  py screen_info.py findall IMAGE_PATH [confidence]")
        print("  py screen_info.py pixel X Y")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "size":
        get_screen_size()

    elif command == "find":
        image_path = sys.argv[2]
        confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.9
        find_on_screen(image_path, confidence)

    elif command == "findall":
        image_path = sys.argv[2]
        confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.9
        find_all_on_screen(image_path, confidence)

    elif command == "pixel":
        x, y = int(sys.argv[2]), int(sys.argv[3])
        get_pixel_color(x, y)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
