"""
UI Element Detection using GroundingDINO
Detects UI elements by natural language description
Superior to color-based detection - understands semantic meaning
"""
import sys
import json
import cv2
import numpy as np
from pathlib import Path

# Check if GroundingDINO is available
try:
    from groundingdino.util.inference import load_model, load_image, predict
    import groundingdino.datasets.transforms as T
    import torch
    HAS_GROUNDING_DINO = True
except ImportError:
    HAS_GROUNDING_DINO = False

# Model cache
_model = None
_device = None

def get_model():
    """Lazy load GroundingDINO model"""
    global _model, _device

    if not HAS_GROUNDING_DINO:
        return None, None

    if _model is None:
        print("Initializing GroundingDINO (first time only)...", file=sys.stderr)

        # Detect device
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {_device}", file=sys.stderr)

        # Load model using groundingdino-py simplified API
        try:
            # Try alternative HuggingFace repo
            from huggingface_hub import hf_hub_download

            # Use IDEA-Research repo
            config_file = hf_hub_download(
                repo_id="IDEA-Research/grounding-dino-tiny",
                filename="GroundingDINO_SwinT_OGC.cfg.py",
                local_dir="./models"
            )
            checkpoint = hf_hub_download(
                repo_id="IDEA-Research/grounding-dino-tiny",
                filename="groundingdino_swint_ogc.pth",
                local_dir="./models"
            )

            _model = load_model(config_file, checkpoint, device=_device)

        except Exception as e:
            print(f"Error loading GroundingDINO model: {e}", file=sys.stderr)
            print("Trying fallback method...", file=sys.stderr)
            try:
                # Fallback: download from alternative source
                import urllib.request
                import os

                model_dir = Path("./models")
                model_dir.mkdir(exist_ok=True)

                config_url = "https://github.com/IDEA-Research/GroundingDINO/raw/main/groundingdino/config/GroundingDINO_SwinT_OGC.py"
                checkpoint_url = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth"

                config_path = model_dir / "GroundingDINO_SwinT_OGC.py"
                checkpoint_path = model_dir / "groundingdino_swint_ogc.pth"

                if not config_path.exists():
                    print(f"Downloading config...", file=sys.stderr)
                    urllib.request.urlretrieve(config_url, config_path)

                if not checkpoint_path.exists():
                    print(f"Downloading checkpoint (~700MB)...", file=sys.stderr)
                    urllib.request.urlretrieve(checkpoint_url, checkpoint_path)

                _model = load_model(str(config_path), str(checkpoint_path), device=_device)

            except Exception as e2:
                print(f"Fallback also failed: {e2}", file=sys.stderr)
                return None, None

    return _model, _device

def detect_ui_elements(
    image_path,
    text_prompt,
    box_threshold=0.35,
    text_threshold=0.25,
    target_y=None,
    y_tolerance=20
):
    """
    Detect UI elements using natural language description

    Args:
        image_path: Path to screenshot
        text_prompt: Natural language description (e.g., "green play button")
        box_threshold: Detection confidence threshold (0-1)
        text_threshold: Text matching threshold (0-1)
        target_y: Optional Y coordinate to filter results
        y_tolerance: Tolerance for Y filtering

    Returns:
        Dict with detected elements and their positions
    """
    if not HAS_GROUNDING_DINO:
        return {
            "error": "GroundingDINO not installed",
            "found": False,
            "install": "pip install groundingdino-py"
        }

    try:
        model, device = get_model()
        if model is None:
            return {"error": "Failed to load model", "found": False}

        # Load and transform image
        image_source, image_tensor = load_image(image_path)

        # Run inference
        boxes, logits, phrases = predict(
            model=model,
            image=image_tensor,
            caption=text_prompt,
            box_threshold=box_threshold,
            text_threshold=text_threshold,
            device=device
        )

        # Convert boxes to pixel coordinates
        h, w, _ = image_source.shape
        boxes = boxes * torch.Tensor([w, h, w, h])

        # Convert to xyxy format
        boxes = boxes.cpu().numpy()
        logits = logits.cpu().numpy()

        results = []

        for box, score, phrase in zip(boxes, logits, phrases):
            x1, y1, x2, y2 = box
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Filter by target Y if specified
            if target_y is not None:
                if abs(center_y - target_y) > y_tolerance:
                    continue

            results.append({
                "phrase": phrase,
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "center": [center_x, center_y],
                "confidence": float(score)
            })

        # Sort by confidence (highest first)
        results.sort(key=lambda x: x["confidence"], reverse=True)

        return {
            "found": len(results) > 0,
            "count": len(results),
            "prompt": text_prompt,
            "detections": results,
            "target_y": target_y
        }

    except Exception as e:
        return {
            "error": str(e),
            "found": False
        }

def click_ui_element(
    image_path,
    text_prompt,
    box_threshold=0.35,
    text_threshold=0.25,
    target_y=None,
    y_tolerance=20
):
    """
    Detect UI element and return click coordinates

    Args:
        image_path: Path to screenshot
        text_prompt: Description of element to click
        box_threshold: Detection confidence threshold
        text_threshold: Text matching threshold
        target_y: Optional Y coordinate filter
        y_tolerance: Y tolerance

    Returns:
        Dict with detection info + click coordinates
    """
    result = detect_ui_elements(
        image_path,
        text_prompt,
        box_threshold,
        text_threshold,
        target_y,
        y_tolerance
    )

    if result.get("found"):
        # Get first (highest confidence) detection
        detection = result["detections"][0]
        result["click_at"] = detection["center"]
        result["should_click"] = True
    else:
        result["should_click"] = False

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "detect": "py detect_ui_grounding.py detect IMAGE 'text prompt' [box_thresh] [text_thresh]",
                "click": "py detect_ui_grounding.py click IMAGE 'text prompt' [box_thresh] [text_thresh]",
                "filter": "py detect_ui_grounding.py filter IMAGE 'text prompt' target_y [y_tolerance]"
            },
            "examples": {
                "detect": "py detect_ui_grounding.py detect temp.png 'green play button'",
                "click": "py detect_ui_grounding.py click temp.png 'circular play icon'",
                "filter": "py detect_ui_grounding.py filter temp.png 'play button' 556 15"
            },
            "note": "Uses GroundingDINO for semantic UI element detection"
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "detect":
        image = sys.argv[2]
        prompt = sys.argv[3]
        box_thresh = float(sys.argv[4]) if len(sys.argv) > 4 else 0.35
        text_thresh = float(sys.argv[5]) if len(sys.argv) > 5 else 0.25
        result = detect_ui_elements(image, prompt, box_thresh, text_thresh)

    elif command == "click":
        image = sys.argv[2]
        prompt = sys.argv[3]
        box_thresh = float(sys.argv[4]) if len(sys.argv) > 4 else 0.35
        text_thresh = float(sys.argv[5]) if len(sys.argv) > 5 else 0.25
        result = click_ui_element(image, prompt, box_thresh, text_thresh)

    elif command == "filter":
        image = sys.argv[2]
        prompt = sys.argv[3]
        target_y = int(sys.argv[4]) if len(sys.argv) > 4 else None
        y_tolerance = int(sys.argv[5]) if len(sys.argv) > 5 else 20
        result = click_ui_element(image, prompt, target_y=target_y, y_tolerance=y_tolerance)

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
