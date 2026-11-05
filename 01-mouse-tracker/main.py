"""Mouse Tracker
Live-prints the mouse coordinates and the RGB / HEX colour under the cursor.
Press Ctrl+C in the terminal to stop.
"""
import time

import pyautogui

REFRESH_SECONDS = 0.05  # 20 updates per second


def color_under_cursor(x, y):
    """Return (r, g, b) of the pixel at x, y or None if it cannot be read."""
    try:
        return pyautogui.pixel(x, y)
    except (OSError, ValueError):
        # Happens on some multi-monitor setups or at the extreme screen edge.
        return None


def main():
    width, height = pyautogui.size()
    print(f"Screen size: {width} x {height}")
    print("Move the mouse around. Press Ctrl+C to stop.\n")
    try:
        while True:
            x, y = pyautogui.position()
            rgb = color_under_cursor(x, y)
            if rgb:
                r, g, b = rgb[:3]
                color = f"RGB({r:>3}, {g:>3}, {b:>3})  #{r:02X}{g:02X}{b:02X}"
            else:
                color = "RGB(n/a)"
            # \r rewrites the same line instead of scrolling the terminal.
            print(f"\rX: {x:>4}  Y: {y:>4}  {color}   ", end="", flush=True)
            time.sleep(REFRESH_SECONDS)
    except KeyboardInterrupt:
        print("\n\nStopped. Bye!")


if __name__ == "__main__":
    main()
