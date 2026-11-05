"""Paint Artist
Opens MS Paint and draws a square, a circle and a spiral by dragging the mouse.
Move the mouse to a screen corner to abort (PyAutoGUI fail-safe).
"""
import argparse
import math
import subprocess
import time

import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.005  # very small pause between mouse events


def drag_path(points, step_duration=0.01):
    """Press the left button at the first point and drag through all the others."""
    x0, y0 = points[0]
    pyautogui.moveTo(x0, y0)
    pyautogui.mouseDown()
    try:
        for x, y in points[1:]:
            pyautogui.moveTo(x, y, duration=step_duration)
    finally:
        pyautogui.mouseUp()


def square_points(cx, cy, size):
    half = size / 2
    return [
        (cx - half, cy - half),
        (cx + half, cy - half),
        (cx + half, cy + half),
        (cx - half, cy + half),
        (cx - half, cy - half),
    ]


def circle_points(cx, cy, radius, steps=72):
    return [
        (cx + radius * math.cos(2 * math.pi * i / steps),
         cy + radius * math.sin(2 * math.pi * i / steps))
        for i in range(steps + 1)
    ]


def spiral_points(cx, cy, max_radius, turns=4, steps_per_turn=40):
    total = turns * steps_per_turn
    return [
        (cx + max_radius * (i / total) * math.cos(2 * math.pi * i / steps_per_turn),
         cy + max_radius * (i / total) * math.sin(2 * math.pi * i / steps_per_turn))
        for i in range(total + 1)
    ]


def main():
    parser = argparse.ArgumentParser(description="Draw shapes in MS Paint")
    parser.add_argument("--size", type=int, default=0,
                        help="shape size in pixels (default: 18%% of the screen height)")
    args = parser.parse_args()

    screen_w, screen_h = pyautogui.size()
    size = args.size or int(screen_h * 0.18)

    print("Starting in 3 seconds - don't touch the mouse...")
    time.sleep(3)

    subprocess.Popen(["mspaint.exe"])
    time.sleep(3)
    pyautogui.hotkey("win", "up")  # maximise Paint so the canvas is big
    time.sleep(1)

    # Make sure the Pencil is selected: click on the canvas area first-time focus.
    cy = int(screen_h * 0.58)
    left_cx = int(screen_w * 0.25)
    mid_cx = int(screen_w * 0.50)
    right_cx = int(screen_w * 0.75)

    print("Drawing square...")
    drag_path(square_points(left_cx, cy, size))
    print("Drawing circle...")
    drag_path(circle_points(mid_cx, cy, size / 2))
    print("Drawing spiral...")
    drag_path(spiral_points(right_cx, cy, size / 2))

    print("Done! Save it with Ctrl+S if you like it.")


if __name__ == "__main__":
    main()
