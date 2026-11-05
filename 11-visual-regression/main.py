"""Visual Regression
Save a baseline screenshot, then compare fresh screenshots against it with PIL.ImageChops.

    python main.py baseline                 # take + store the baseline
    python main.py compare                  # take a screenshot and diff it against the baseline
    python main.py compare --max-diff 1.0   # allow up to 1% of pixels to differ
    python main.py baseline --region 0 0 1280 720 --delay 5

Exit code is 0 on PASS and 1 on FAIL, so it works in Task Scheduler / CI too.
"""
import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import pyautogui
from PIL import Image, ImageChops

BASELINE = Path("baselines") / "baseline.png"
CAPTURES = Path("captures")
DIFFS = Path("diffs")


def grab(region, delay):
    if delay:
        print(f"Capturing in {delay:g}s - get your page on screen...")
        time.sleep(delay)
    return pyautogui.screenshot(region=tuple(region) if region else None)


def compare_images(baseline, current, tolerance=10):
    """Return (percent_changed, bounding_box, highlighted_image).

    tolerance: per-pixel brightness difference (0-255) ignored as noise (anti-aliasing etc.).
    """
    a = baseline.convert("RGB")
    b = current.convert("RGB")
    if a.size != b.size:
        raise ValueError(f"Size mismatch: baseline {a.size} vs current {b.size}")

    diff = ImageChops.difference(a, b).convert("L")
    mask = diff.point(lambda p: 255 if p > tolerance else 0)
    changed = mask.histogram()[255]
    percent = changed / (a.width * a.height) * 100
    red = Image.new("RGB", b.size, (255, 0, 0))
    highlighted = Image.composite(red, b, mask)  # changed pixels painted red
    return percent, mask.getbbox(), highlighted


def cmd_baseline(args):
    BASELINE.parent.mkdir(exist_ok=True)
    grab(args.region, args.delay).save(BASELINE)
    print(f"Baseline saved: {BASELINE}")


def cmd_compare(args):
    if not BASELINE.exists():
        sys.exit("No baseline yet - run:  python main.py baseline")
    CAPTURES.mkdir(exist_ok=True)
    DIFFS.mkdir(exist_ok=True)

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current = grab(args.region, args.delay)
    capture_path = CAPTURES / f"capture_{stamp}.png"
    current.save(capture_path)

    try:
        percent, bbox, highlighted = compare_images(
            Image.open(BASELINE), current, tolerance=args.tolerance)
    except ValueError as exc:
        print(f"FAIL: {exc}\nUse the same --region as the baseline.")
        sys.exit(1)

    diff_path = DIFFS / f"diff_{stamp}.png"
    highlighted.save(diff_path)

    print(f"Changed pixels: {percent:.3f}%  (limit {args.max_diff}%)")
    print(f"Changed area  : {bbox if bbox else 'none'}")
    print(f"Capture: {capture_path}\nDiff   : {diff_path}")
    if percent > args.max_diff:
        print("RESULT: FAIL - the page looks different from the baseline.")
        sys.exit(1)
    print("RESULT: PASS")


def main():
    parser = argparse.ArgumentParser(description="Screenshot baseline + comparison")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func in (("baseline", cmd_baseline), ("compare", cmd_compare)):
        p = sub.add_parser(name)
        p.add_argument("--region", nargs=4, type=int, metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"),
                       help="only capture this part of the screen")
        p.add_argument("--delay", type=float, default=0, help="seconds to wait before capturing")
        if name == "compare":
            p.add_argument("--max-diff", type=float, default=0.5, help="max %% of pixels allowed to change")
            p.add_argument("--tolerance", type=int, default=10, help="ignore per-pixel differences up to this value")
        p.set_defaults(func=func)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
