"""Screenshot Logger
Takes a screenshot every N seconds (default 30) and saves it with a timestamped name.
Press Ctrl+C to stop.

Examples:
    python main.py
    python main.py --interval 10 --count 6 --folder shots
"""
import argparse
import time
from datetime import datetime
from pathlib import Path

import pyautogui


def take_screenshot(folder):
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = Path(folder) / f"screenshot_{stamp}.png"
    pyautogui.screenshot(str(path))
    return path


def main():
    parser = argparse.ArgumentParser(description="Timestamped screenshot logger")
    parser.add_argument("--interval", type=float, default=30, help="seconds between shots")
    parser.add_argument("--count", type=int, default=0, help="stop after N shots (0 = run forever)")
    parser.add_argument("--folder", default="screenshots", help="where to save the images")
    args = parser.parse_args()

    Path(args.folder).mkdir(parents=True, exist_ok=True)
    print(f"Saving a screenshot every {args.interval:g}s into '{args.folder}'. Ctrl+C to stop.")

    taken = 0
    next_run = time.monotonic()
    try:
        while args.count == 0 or taken < args.count:
            path = take_screenshot(args.folder)
            taken += 1
            print(f"[{taken}] saved {path}")
            next_run += args.interval  # fixed schedule, so saving time doesn't cause drift
            time.sleep(max(0, next_run - time.monotonic()))
    except KeyboardInterrupt:
        print("\nStopped by user.")
    print(f"Total screenshots: {taken}")


if __name__ == "__main__":
    main()
