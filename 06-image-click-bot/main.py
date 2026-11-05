"""Image-Click Bot
Waits for a button image to appear on screen, clicks it, and repeats.

First capture a template:   python capture_template.py
Then run the bot:           python main.py templates/button.png --repeat 5
"""
import argparse
import time

import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

NotFound = getattr(pyautogui, "ImageNotFoundException", Exception)


def find_image(image, confidence=0.85, region=None, grayscale=True):
    """Return the centre (x, y) of the image on screen, or None."""
    try:
        return pyautogui.locateCenterOnScreen(
            image, confidence=confidence, region=region, grayscale=grayscale)
    except NotFound:
        return None


def wait_for_image(image, timeout=30, interval=0.5, **kwargs):
    """Poll until the image appears. Returns its centre or None on timeout."""
    end = time.time() + timeout
    while time.time() < end:
        pos = find_image(image, **kwargs)
        if pos:
            return pos
        time.sleep(interval)
    return None


def wait_until_gone(image, timeout=5, interval=0.3, **kwargs):
    end = time.time() + timeout
    while time.time() < end:
        if not find_image(image, **kwargs):
            return True
        time.sleep(interval)
    return False


def main():
    parser = argparse.ArgumentParser(description="Wait for an image, click it, repeat")
    parser.add_argument("image", help="path to the template PNG (e.g. templates/button.png)")
    parser.add_argument("--repeat", type=int, default=1, help="how many clicks (0 = forever)")
    parser.add_argument("--timeout", type=float, default=30, help="seconds to wait for each appearance")
    parser.add_argument("--confidence", type=float, default=0.85, help="match threshold 0-1")
    parser.add_argument("--pause", type=float, default=1.0, help="seconds to rest between rounds")
    args = parser.parse_args()

    done = 0
    print(f"Looking for '{args.image}'. Move the mouse to a corner to abort.")
    try:
        while args.repeat == 0 or done < args.repeat:
            pos = wait_for_image(args.image, timeout=args.timeout, confidence=args.confidence)
            if not pos:
                print(f"Timed out after {args.timeout:g}s - the button never appeared.")
                break
            pyautogui.click(pos)
            done += 1
            print(f"[{done}] clicked at {tuple(pos)}")
            # Give the UI time to react (button usually disappears) so we don't double-click it.
            wait_until_gone(args.image, confidence=args.confidence)
            time.sleep(args.pause)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    print(f"Total clicks: {done}")


if __name__ == "__main__":
    main()
