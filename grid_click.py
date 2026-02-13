"""
Grid-based clicking system
Uses grid coordinates instead of absolute pixels for better accuracy
"""
import pyautogui
import sys
import json

GRID_SIZE = 100  # Must match grid_overlay.py

def grid_to_pixel(col, row, grid_size=GRID_SIZE):
    """Convert grid cell (col, row) to pixel coordinates (center of cell)"""
    x = col * grid_size + grid_size // 2
    y = row * grid_size + grid_size // 2
    return x, y

def pixel_to_grid(x, y, grid_size=GRID_SIZE):
    """Convert pixel coordinates to grid cell"""
    col = x // grid_size
    row = y // grid_size
    return col, row

def click_grid(col, row, duration=0.5):
    """Click at grid coordinates"""
    x, y = grid_to_pixel(col, row)
    pyautogui.click(x, y, duration=duration)
    return {"clicked": True, "grid": (col, row), "pixel": (x, y)}

def move_grid(col, row, duration=0.5):
    """Move mouse to grid coordinates"""
    x, y = grid_to_pixel(col, row)
    pyautogui.moveTo(x, y, duration=duration)
    return {"moved": True, "grid": (col, row), "pixel": (x, y)}

def get_mouse_grid():
    """Get current mouse position in grid coordinates"""
    x, y = pyautogui.position()
    col, row = pixel_to_grid(x, y)
    return {
        "pixel": (x, y),
        "grid": (col, row),
        "cell_center": grid_to_pixel(col, row)
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage:",
            "commands": {
                "click": "py grid_click.py click COL ROW",
                "move": "py grid_click.py move COL ROW",
                "pos": "py grid_click.py pos",
                "convert": "py grid_click.py convert X Y (pixel to grid)",
                "toPixel": "py grid_click.py toPixel COL ROW (grid to pixel)"
            },
            "example": "py grid_click.py click 4 2  (clicks center of cell 4,2)"
        }, indent=2))
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "click":
        col, row = int(sys.argv[2]), int(sys.argv[3])
        result = click_grid(col, row)

    elif command == "move":
        col, row = int(sys.argv[2]), int(sys.argv[3])
        result = move_grid(col, row)

    elif command == "pos":
        result = get_mouse_grid()

    elif command == "convert":
        x, y = int(sys.argv[2]), int(sys.argv[3])
        col, row = pixel_to_grid(x, y)
        result = {"pixel": (x, y), "grid": (col, row)}

    elif command == "topixel":
        col, row = int(sys.argv[2]), int(sys.argv[3])
        x, y = grid_to_pixel(col, row)
        result = {"grid": (col, row), "pixel": (x, y)}

    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2))
