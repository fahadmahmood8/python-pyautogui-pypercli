"""Capture a template image of the button you want the bot to click.

1. Run this script.
2. Hover the mouse over the TOP-LEFT corner of the button and wait.
3. Hover over the BOTTOM-RIGHT corner and wait.
The cropped image is saved to templates/<name>.png
"""
import argparse
import time
from pathlib import Path

import pyautogui


def countdown(label, seconds=4):
    for s in range(seconds, 0, -1):
        print(f"  {label} in {s}...", end="\r", flush=True)
        time.sleep(1)
    pos = pyautogui.position()
    print(f"  {label}: captured {tuple(pos)}      ")
    return pos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="button", help="file name without extension")
    args = parser.parse_args()

    print("Hover over the TOP-LEFT corner of the button...")
    x1, y1 = countdown("top-left")
    print("Now hover over the BOTTOM-RIGHT corner...")
    x2, y2 = countdown("bottom-right")

    left, top = min(x1, x2), min(y1, y2)
    width, height = abs(x2 - x1), abs(y2 - y1)
    if width < 4 or height < 4:
        print("The region is too small - try again.")
        return

    Path("templates").mkdir(exist_ok=True)
    out = Path("templates") / f"{args.name}.png"
    pyautogui.screenshot(str(out), region=(left, top, width, height))
    print(f"Saved {out} ({width}x{height}px)")


if __name__ == "__main__":
    main()
