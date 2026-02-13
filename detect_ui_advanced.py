"""
Advanced UI Detection using OpenCV
Detects buttons, icons, and UI elements by shape, color, and pattern
Lightweight and fast alternative to heavy ML models
"""
import cv2
import numpy as np
import sys
import json

def detect_circular_buttons_all_colors(image_path, target_y=None, tolerance=20, min_radius=5, max_radius=30):
    """
    Detect ALL circular buttons regardless of color using edge detection

    Args:
        image_path: Path to screenshot
        target_y: Y coordinate to search near
        tolerance: Y coordinate tolerance
        min_radius: Minimum circle radius
        max_radius: Maximum circle radius

    Returns:
        List of detected circles with colors
    """
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Could not load image", "buttons": []}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect circles using Hough Transform
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

            # Filter by target Y if specified
            if target_y is not None:
                if abs(y - target_y) > tolerance:
                    continue

            # Extract dominant color in circle
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)
            mean_color = cv2.mean(img, mask=mask)[:3]

            # Determine color name
            b, g, r_val = mean_color
            color_name = get_color_name(r_val, g, b)

            results.append({
                "center": [x, y],
                "radius": r,
                "bbox": [x-r, y-r, x+r, y+r],
                "color": color_name,
                "rgb": [int(r_val), int(g), int(b)]
            })

    results.sort(key=lambda c: c["center"][0])

    return {
        "found": len(results) > 0,
        "count": len(results),
        "buttons": results,
        "target_y": target_y
    }

def get_color_name(r, g, b):
    """Determine color name from RGB values"""
    # Normalize
    total = r + g + b
    if total < 50:
        return "black"
    if total > 700:
        return "white"

    # Dominant color with improved thresholds
    # Red detection
    if r > g * 1.5 and r > b * 1.5:
        if g > 100:
            return "orange"
        return "red"

    # Green detection (improved to distinguish from cyan)
    elif g > b * 1.15 and g > r * 1.1:
        # Green is clearly dominant over blue and red
        return "green"

    # Blue detection
    elif b > r * 1.5 and b > g * 1.5:
        return "blue"

    # Yellow detection
    elif r > 150 and g > 150 and b < 100:
        return "yellow"

    # Purple detection
    elif r > 100 and g < 80 and b > 100:
        return "purple"

    # Cyan detection (blue and green both high, but blue slightly higher)
    elif b > g * 0.9 and b > r * 1.3 and g > r * 1.3:
        return "cyan"

    # Gray/neutral
    else:
        return "gray"

def detect_shapes(image_path, target_y=None, tolerance=20, min_area=100):
    """
    Detect common UI shapes: circles, rectangles, triangles

    Args:
        image_path: Path to screenshot
        target_y: Y coordinate filter
        tolerance: Y tolerance
        min_area: Minimum shape area

    Returns:
        Dict with detected shapes and their properties
    """
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Could not load image", "shapes": []}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    results = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        # Get bounding box
        x, y, w, h = cv2.boundingRect(contour)
        center_x = x + w // 2
        center_y = y + h // 2

        # Filter by target Y
        if target_y is not None:
            if abs(center_y - target_y) > tolerance:
                continue

        # Approximate shape
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = len(approx)

        # Determine shape type
        if vertices == 3:
            shape_type = "triangle"
        elif vertices == 4:
            aspect_ratio = float(w) / h
            shape_type = "square" if 0.95 <= aspect_ratio <= 1.05 else "rectangle"
        elif vertices > 8:
            shape_type = "circle"
        else:
            shape_type = f"polygon-{vertices}"

        # Get dominant color
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mean_color = cv2.mean(img, mask=mask)[:3]
        b, g, r = mean_color
        color_name = get_color_name(r, g, b)

        results.append({
            "shape": shape_type,
            "center": [center_x, center_y],
            "bbox": [x, y, x+w, y+h],
            "size": [w, h],
            "area": int(area),
            "vertices": vertices,
            "color": color_name,
            "rgb": [int(r), int(g), int(b)]
        })

    results.sort(key=lambda s: s["center"][0])

    return {
        "found": len(results) > 0,
        "count": len(results),
        "shapes": results,
        "target_y": target_y
    }

def find_button(image_path, color=None, shape=None, target_y=None, tolerance=20):
    """
    Find button matching criteria (color and/or shape)

    Args:
        image_path: Path to screenshot
        color: Target color ("red", "green", "blue", etc.) or None for any
        shape: Target shape ("circle", "triangle", "rectangle") or None for any
        target_y: Y coordinate filter
        tolerance: Y tolerance

    Returns:
        Dict with matching buttons
    """
    # Detect by shape if specified
    if shape == "circle":
        result = detect_circular_buttons_all_colors(image_path, target_y, tolerance)
        buttons = result.get("buttons", [])
    else:
        result = detect_shapes(image_path, target_y, tolerance)
        buttons = result.get("shapes", [])

    # Filter by color if specified
    if color:
        buttons = [b for b in buttons if b.get("color", "").lower() == color.lower()]

    # Filter by shape if specified and not already filtered
    if shape and shape != "circle":
        buttons = [b for b in buttons if shape.lower() in b.get("shape", "").lower()]

    return {
        "found": len(buttons) > 0,
        "count": len(buttons),
        "matches": buttons,
        "filter": {
            "color": color,
            "shape": shape,
            "target_y": target_y
        }
    }

def smart_detect(image_path, description, target_y=None, tolerance=20):
    """
    Smart detection based on natural language description
    Parses description to extract color and shape hints

    Args:
        image_path: Path to screenshot
        description: Natural description like "green circular play button"
        target_y: Y coordinate filter
        tolerance: Y tolerance

    Returns:
        Dict with best matching elements
    """
    desc_lower = description.lower()

    # Extract color
    color = None
    for c in ["red", "green", "blue", "yellow", "orange", "purple", "cyan", "white", "black", "gray"]:
        if c in desc_lower:
            color = c
            break

    # Extract shape
    shape = None
    if "circle" in desc_lower or "circular" in desc_lower or "round" in desc_lower:
        shape = "circle"
    elif "triangle" in desc_lower or "play" in desc_lower:
        shape = "triangle"
    elif "square" in desc_lower or "rectangle" in desc_lower or "box" in desc_lower:
        shape = "rectangle"

    # Find matching buttons
    result = find_button(image_path, color, shape, target_y, tolerance)
    result["description"] = description
    result["parsed"] = {"color": color, "shape": shape}

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "circles": "py detect_ui_advanced.py circles IMAGE [target_y] [tolerance]",
                "shapes": "py detect_ui_advanced.py shapes IMAGE [target_y] [tolerance]",
                "find": "py detect_ui_advanced.py find IMAGE [color] [shape] [target_y]",
                "smart": "py detect_ui_advanced.py smart IMAGE 'description' [target_y]"
            },
            "examples": {
                "circles": "py detect_ui_advanced.py circles temp.png 556 15",
                "shapes": "py detect_ui_advanced.py shapes temp.png",
                "find": "py detect_ui_advanced.py find temp.png green circle 556",
                "smart": "py detect_ui_advanced.py smart temp.png 'green circular play button' 556"
            },
            "note": "Fast OpenCV-based detection - no model download required"
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "circles":
        image = sys.argv[2]
        target_y = int(sys.argv[3]) if len(sys.argv) > 3 else None
        tolerance = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        result = detect_circular_buttons_all_colors(image, target_y, tolerance)

    elif command == "shapes":
        image = sys.argv[2]
        target_y = int(sys.argv[3]) if len(sys.argv) > 3 else None
        tolerance = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        result = detect_shapes(image, target_y, tolerance)

    elif command == "find":
        image = sys.argv[2]
        color = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].isdigit() else None
        shape = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].isdigit() else None
        target_y = int(sys.argv[5]) if len(sys.argv) > 5 else None
        tolerance = int(sys.argv[6]) if len(sys.argv) > 6 else 20
        result = find_button(image, color, shape, target_y, tolerance)

    elif command == "smart":
        image = sys.argv[2]
        description = sys.argv[3]
        target_y = int(sys.argv[4]) if len(sys.argv) > 4 else None
        tolerance = int(sys.argv[5]) if len(sys.argv) > 5 else 20
        result = smart_detect(image, description, target_y, tolerance)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
