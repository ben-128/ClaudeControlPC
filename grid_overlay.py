"""
Grid Overlay System for Precise Mouse Control
Displays numbered grid over screen for accurate coordinate reference
Based on research: Dragon MouseGrid, R-VLM region-aware approach
"""
import tkinter as tk
import pyautogui
import sys

class GridOverlay:
    def __init__(self, grid_size=100):
        """
        Create a transparent grid overlay over the entire screen
        grid_size: Size of each grid cell in pixels (default 100x100)
        """
        self.grid_size = grid_size
        self.screen_width, self.screen_height = pyautogui.size()

        # Create fullscreen transparent window
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.3)  # 30% opacity
        self.root.configure(bg='black')

        # Make window click-through (Windows only)
        try:
            self.root.attributes('-transparentcolor', 'black')
        except:
            pass

        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack()

        self.draw_grid()

        # ESC to close
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        # Info label
        info = tk.Label(
            self.root,
            text="GRID OVERLAY - Press ESC to close | Grid size: {}px".format(grid_size),
            bg='yellow',
            fg='black',
            font=('Arial', 12, 'bold')
        )
        info.place(x=10, y=10)

    def draw_grid(self):
        """Draw grid lines and labels"""
        cols = (self.screen_width // self.grid_size) + 1
        rows = (self.screen_height // self.grid_size) + 1

        # Draw vertical lines
        for i in range(cols):
            x = i * self.grid_size
            self.canvas.create_line(
                x, 0, x, self.screen_height,
                fill='lime',
                width=2
            )
            # Column number at top
            self.canvas.create_text(
                x + self.grid_size // 2, 20,
                text=str(i),
                fill='yellow',
                font=('Arial', 16, 'bold')
            )

        # Draw horizontal lines
        for i in range(rows):
            y = i * self.grid_size
            self.canvas.create_line(
                0, y, self.screen_width, y,
                fill='lime',
                width=2
            )
            # Row number at left
            self.canvas.create_text(
                20, y + self.grid_size // 2,
                text=str(i),
                fill='yellow',
                font=('Arial', 16, 'bold')
            )

        # Draw cell coordinates
        for row in range(rows):
            for col in range(cols):
                x_center = col * self.grid_size + self.grid_size // 2
                y_center = row * self.grid_size + self.grid_size // 2

                # Skip top-left area where info is displayed
                if row == 0 and col == 0:
                    continue

                # Cell label: (col, row)
                self.canvas.create_text(
                    x_center, y_center,
                    text=f"({col},{row})",
                    fill='cyan',
                    font=('Arial', 10)
                )

    def run(self):
        """Start the overlay"""
        self.root.mainloop()

def grid_to_pixel(col, row, grid_size=100):
    """Convert grid coordinates to pixel coordinates (center of cell)"""
    x = col * grid_size + grid_size // 2
    y = row * grid_size + grid_size // 2
    return x, y

def pixel_to_grid(x, y, grid_size=100):
    """Convert pixel coordinates to grid coordinates"""
    col = x // grid_size
    row = y // grid_size
    return col, row

if __name__ == "__main__":
    if len(sys.argv) > 1:
        grid_size = int(sys.argv[1])
    else:
        grid_size = 100

    print(f"Starting grid overlay with {grid_size}px cells...")
    print("Press ESC to close the overlay")

    overlay = GridOverlay(grid_size)
    overlay.run()
