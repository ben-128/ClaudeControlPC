"""
Demo script showcasing Claude PC Control capabilities
Run this to test that everything works
"""
import pyautogui
import time
import sys

def countdown(seconds):
    """Countdown before starting demo"""
    print(f"\nDemo will start in {seconds} seconds...")
    print("Move mouse to TOP-LEFT corner to abort (failsafe)")
    for i in range(seconds, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Starting!\n")

def demo_screen_info():
    """Demo: Screen information"""
    print("=== DEMO 1: Screen Information ===")
    width, height = pyautogui.size()
    print(f"Screen size: {width}x{height}")

    x, y = pyautogui.position()
    print(f"Current mouse position: ({x}, {y})")

    pixel = pyautogui.pixel(x, y)
    print(f"Pixel color at cursor: RGB{pixel}")
    print()

def demo_mouse():
    """Demo: Mouse movement"""
    print("=== DEMO 2: Mouse Movement ===")

    # Get screen center
    width, height = pyautogui.size()
    center_x, center_y = width // 2, height // 2

    print(f"Moving to screen center ({center_x}, {center_y})...")
    pyautogui.moveTo(center_x, center_y, duration=1)
    time.sleep(0.5)

    print("Drawing a square...")
    pyautogui.move(100, 0, duration=0.5)   # right
    pyautogui.move(0, 100, duration=0.5)   # down
    pyautogui.move(-100, 0, duration=0.5)  # left
    pyautogui.move(0, -100, duration=0.5)  # up
    print()

def demo_keyboard():
    """Demo: Keyboard typing (opens Notepad)"""
    print("=== DEMO 3: Keyboard Demo ===")
    print("Opening Notepad...")

    # Open Run dialog (Win+R)
    pyautogui.hotkey('win', 'r')
    time.sleep(0.5)

    # Type 'notepad' and press Enter
    pyautogui.write('notepad', interval=0.1)
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(1)

    # Type demo text
    print("Typing in Notepad...")
    pyautogui.write('Hello from Claude PC Control!', interval=0.05)
    pyautogui.press('enter', presses=2)
    pyautogui.write('This is a demonstration of GUI automation.', interval=0.05)
    pyautogui.press('enter')
    pyautogui.write('I can control mouse, keyboard, and take screenshots!', interval=0.05)

    print("\nNotepad opened with demo text!")
    print("(Close Notepad manually - don't save)")
    print()

def demo_screenshot():
    """Demo: Take a screenshot"""
    print("=== DEMO 4: Screenshot ===")
    filename = "demo_screenshot.png"
    print(f"Taking screenshot: {filename}")
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")
    print("You can now read this file with Claude's Read tool!")
    print()

def main():
    print("=" * 50)
    print("CLAUDE PC CONTROL - DEMO")
    print("=" * 50)

    if "--skip-countdown" not in sys.argv:
        countdown(3)

    try:
        demo_screen_info()
        time.sleep(1)

        demo_mouse()
        time.sleep(1)

        if "--no-notepad" not in sys.argv:
            response = input("Open Notepad for keyboard demo? (y/n): ")
            if response.lower() == 'y':
                demo_keyboard()
                time.sleep(1)

        demo_screenshot()

        print("=" * 50)
        print("DEMO COMPLETE!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Use screenshot.py to capture screen")
        print("2. Use mouse_control.py to move/click")
        print("3. Use keyboard_control.py to type/press keys")
        print("4. Use screen_info.py to find images on screen")

    except pyautogui.FailSafeException:
        print("\n[ABORTED] Mouse moved to corner - failsafe triggered")
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    main()
