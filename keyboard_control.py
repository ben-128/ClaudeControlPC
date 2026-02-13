"""
Keyboard control utility for Claude
Type text and send key combinations
"""
import pyautogui
import sys
import time

def type_text(text, interval=0.05):
    """Type text with optional interval between keys"""
    print(f"Typing: {text}")
    pyautogui.write(text, interval=interval)

def press_key(key, presses=1):
    """Press a single key"""
    print(f"Pressing key: {key} ({presses}x)")
    pyautogui.press(key, presses=presses)

def hotkey(*keys):
    """Press a combination of keys (e.g., ctrl+c)"""
    print(f"Pressing hotkey: {'+'.join(keys)}")
    pyautogui.hotkey(*keys)

def hold_key(key, duration=1.0):
    """Hold a key for a duration"""
    print(f"Holding key: {key} for {duration}s")
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  py keyboard_control.py type 'text to type'")
        print("  py keyboard_control.py press KEY [count]")
        print("  py keyboard_control.py hotkey KEY1 KEY2 ...")
        print("  py keyboard_control.py hold KEY [duration]")
        print("\nCommon keys:")
        print("  enter, tab, esc, space, backspace, delete")
        print("  up, down, left, right")
        print("  ctrl, alt, shift, win")
        print("  f1-f12, a-z, 0-9")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "type":
        text = ' '.join(sys.argv[2:])
        interval = 0.05  # Can be made configurable
        type_text(text, interval)

    elif command == "press":
        key = sys.argv[2]
        presses = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        press_key(key, presses)

    elif command == "hotkey":
        keys = sys.argv[2:]
        hotkey(*keys)

    elif command == "hold":
        key = sys.argv[2]
        duration = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        hold_key(key, duration)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
