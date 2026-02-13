"""
Icon Detection using OpenCV
Detects circular buttons, play icons, etc. by shape and color
"""
import cv2
import numpy as np
import sys
import json

def detect_circular_buttons(image_path, target_y=None, tolerance=20, min_radius=5, max_radius=30):
    """
    Detect circular buttons (like play icons) in screenshot

    Args:
        image_path: Path to screenshot
        target_y: Y coordinate to search near (e.g., text line Y position)
        tolerance: Y coordinate tolerance in pixels
        min_radius: Minimum circle radius
        max_radius: Maximum circle radius

    Returns:
        List of detected circles with positions
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Could not load image", "circles": []}

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=min_radius,
        maxRadius=max_radius
    )

    results = []

    if circles is not None:
        circles = np.uint16(np.around(circles))

        for circle in circles[0, :]:
            x, y, r = int(circle[0]), int(circle[1]), int(circle[2])

            # If target_y specified, only return circles near that Y coordinate
            if target_y is not None:
                if abs(y - target_y) > tolerance:
                    continue

            results.append({
                "center": [x, y],
                "radius": r,
                "bbox": [x-r, y-r, x+r, y+r]
            })

    # Sort by X coordinate (left to right)
    results.sort(key=lambda c: c["center"][0])

    return {
        "found": len(results) > 0,
        "count": len(results),
        "circles": results,
        "target_y": target_y
    }

def detect_red_buttons(image_path, target_y=None, tolerance=20, min_area=50):
    """
    Detect red circular buttons specifically

    Args:
        image_path: Path to screenshot
        target_y: Y coordinate to search near
        tolerance: Y coordinate tolerance
        min_area: Minimum button area in pixels

    Returns:
        List of detected red buttons with positions
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Could not load image", "buttons": []}

    # Convert BGR to HSV for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range for red color (red wraps around in HSV)
    # Lower red range
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    # Upper red range
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    results = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2

        # Filter by target Y if specified
        if target_y is not None:
            if abs(center_y - target_y) > tolerance:
                continue

        # Check if roughly circular (aspect ratio close to 1)
        aspect_ratio = float(w) / h if h > 0 else 0
        if 0.7 < aspect_ratio < 1.3:  # Roughly square/circular
            results.append({
                "center": [center_x, center_y],
                "bbox": [x, y, x+w, y+h],
                "area": int(area),
                "size": [w, h]
            })

    # Sort by X coordinate (left to right)
    results.sort(key=lambda b: b["center"][0])

    return {
        "found": len(results) > 0,
        "count": len(results),
        "buttons": results,
        "target_y": target_y
    }

def detect_green_buttons(image_path, target_y=None, tolerance=20, min_area=50):
    """
    Detect green circular buttons specifically

    Args:
        image_path: Path to screenshot
        target_y: Y coordinate to search near
        tolerance: Y coordinate tolerance
        min_area: Minimum button area in pixels

    Returns:
        List of detected green buttons with positions
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Could not load image", "buttons": []}

    # Convert BGR to HSV for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range for green color in HSV
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # Create mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    results = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2

        # Filter by target Y if specified
        if target_y is not None:
            if abs(center_y - target_y) > tolerance:
                continue

        # Check if roughly circular (aspect ratio close to 1)
        aspect_ratio = float(w) / h if h > 0 else 0
        if 0.7 < aspect_ratio < 1.3:  # Roughly square/circular
            results.append({
                "center": [center_x, center_y],
                "bbox": [x, y, x+w, y+h],
                "area": int(area),
                "size": [w, h]
            })

    # Sort by X coordinate (left to right)
    results.sort(key=lambda b: b["center"][0])

    return {
        "found": len(results) > 0,
        "count": len(results),
        "buttons": results,
        "target_y": target_y
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "circles": "py detect_icons.py circles IMAGE [target_y] [tolerance]",
                "red": "py detect_icons.py red IMAGE [target_y] [tolerance]",
                "green": "py detect_icons.py green IMAGE [target_y] [tolerance]"
            },
            "note": "Detects icon buttons by shape and color"
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "circles":
        image = sys.argv[2]
        target_y = int(sys.argv[3]) if len(sys.argv) > 3 else None
        tolerance = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        result = detect_circular_buttons(image, target_y, tolerance)

    elif command == "red":
        image = sys.argv[2]
        target_y = int(sys.argv[3]) if len(sys.argv) > 3 else None
        tolerance = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        result = detect_red_buttons(image, target_y, tolerance)

    elif command == "green":
        image = sys.argv[2]
        target_y = int(sys.argv[3]) if len(sys.argv) > 3 else None
        tolerance = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        result = detect_green_buttons(image, target_y, tolerance)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
