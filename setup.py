"""
Setup script for Claude PC Control
Installs required dependencies for GUI automation
"""
import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("=== Claude PC Control Setup ===")
    print("Installing required packages...\n")

    packages = [
        "pyautogui",      # GUI automation (mouse, keyboard, screenshots)
        "pillow",         # Image processing (required by pyautogui)
        "opencv-python",  # Advanced image recognition (optional)
        "pytesseract",    # OCR for text recognition (optional)
    ]

    for package in packages:
        try:
            install_package(package)
            print(f"[OK] {package} installed successfully\n")
        except Exception as e:
            print(f"[ERROR] Failed to install {package}: {e}\n")

    print("=== Setup Complete ===")
    print("Run 'py -3 demo.py' to test the installation")

if __name__ == "__main__":
    main()
