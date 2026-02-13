"""
Simplified OmniParser Wrapper for Python 3.14
Uses YOLO for UI element detection without full OmniParser dependencies
"""
import sys
import json
from pathlib import Path

try:
    from ultralytics import YOLO
    import cv2
    import numpy as np
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False

def detect_ui_elements(image_path, conf_threshold=0.25):
    """
    Detect UI elements using YOLO
    Returns list of detected elements with bounding boxes
    """
    if not HAS_YOLO:
        return {"error": "YOLOv8 not installed", "elements": []}

    # For now, use standard YOLO model
    # TODO: Download OmniParser's fine-tuned model for UI detection
    model_path = Path("yolov8n.pt")  # Lightweight model

    if not model_path.exists():
        print("Downloading YOLOv8 model...")
        model = YOLO("yolov8n.pt")
    else:
        model = YOLO(str(model_path))

    # Run detection
    results = model(image_path, conf=conf_threshold)

    elements = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            elements.append({
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "center": [int((x1 + x2) / 2), int((y1 + y2) / 2)],
                "confidence": conf,
                "class": cls,
                "label": model.names[cls]
            })

    return {
        "found": len(elements) > 0,
        "count": len(elements),
        "elements": elements
    }

def annotate_screenshot(image_path, elements, output_path="temp_annotated.png"):
    """
    Draw bounding boxes and labels on screenshot (Set-of-Mark style)
    """
    img = cv2.imread(image_path)

    for i, elem in enumerate(elements):
        bbox = elem["bbox"]
        x1, y1, x2, y2 = bbox

        # Draw bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw element number
        label = f"#{i+1}"
        cv2.putText(img, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imwrite(output_path, img)
    return output_path

def click_element(elements, element_id):
    """
    Get click coordinates for a specific element ID
    """
    if element_id < 1 or element_id > len(elements):
        return {"error": f"Element #{element_id} not found"}

    elem = elements[element_id - 1]
    return {
        "element_id": element_id,
        "center": elem["center"],
        "bbox": elem["bbox"],
        "label": elem.get("label", "unknown")
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "detect": "py omni_simple.py detect IMAGE_PATH",
                "annotate": "py omni_simple.py annotate IMAGE_PATH [OUTPUT]",
                "click": "py omni_simple.py click IMAGE_PATH ELEMENT_ID"
            },
            "note": "Full OmniParser requires Python 3.8-3.11. This is a simplified version."
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "detect":
        image_path = sys.argv[2]
        result = detect_ui_elements(image_path)
        print(json.dumps(result, indent=2))

    elif command == "annotate":
        image_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else "temp_annotated.png"

        # Detect elements
        result = detect_ui_elements(image_path)

        if result["found"]:
            # Annotate image
            annotated = annotate_screenshot(image_path, result["elements"], output_path)
            print(json.dumps({
                "annotated": True,
                "output": annotated,
                "elements_found": result["count"]
            }, indent=2))
        else:
            print(json.dumps({"error": "No elements detected"}, indent=2))

    elif command == "click":
        image_path = sys.argv[2]
        element_id = int(sys.argv[3])

        # Detect elements
        result = detect_ui_elements(image_path)

        if result["found"]:
            # Get click coords
            click_result = click_element(result["elements"], element_id)
            print(json.dumps(click_result, indent=2))
        else:
            print(json.dumps({"error": "No elements detected"}, indent=2))

    else:
        print(json.dumps({"error": f"Unknown command: {command}"}, indent=2))
