"""Upload + Verify Bot
Clicks "Choose File", fills the native file dialog, submits, then verifies the file really
arrived in your server's uploads/ folder.

Example (WAMP + the bundled demo/index.php copied to C:\\wamp64\\www\\upload-demo):
    python main.py --file sample_upload.txt ^
        --url http://localhost/upload-demo/ ^
        --choose-xy 600 350 --submit-xy 600 420 ^
        --uploads-dir C:\\wamp64\\www\\upload-demo\\uploads
"""
import argparse
import hashlib
import sys
import time
import webbrowser
from pathlib import Path

import pyautogui
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

NotFound = getattr(pyautogui, "ImageNotFoundException", Exception)


def paste_text(text, pause=0.15):
    pyperclip.copy(text)
    time.sleep(pause)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(pause)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def click_target(image=None, xy=None, timeout=10):
    """Click an on-screen image (preferred) or fixed coordinates."""
    if image:
        end = time.time() + timeout
        while time.time() < end:
            try:
                pos = pyautogui.locateCenterOnScreen(image, confidence=0.85, grayscale=True)
            except NotFound:
                pos = None
            if pos:
                pyautogui.click(pos)
                return True
            time.sleep(0.4)
        return False
    if xy:
        pyautogui.click(*xy)
        return True
    return False


def verify_upload(source, uploads_dir, started_at, timeout=10):
    """Wait until the file shows up in uploads_dir. Matches by name first, then by content hash
    (many servers rename uploads). Returns the matching Path or None."""
    uploads_dir = Path(uploads_dir)
    source_hash = sha256(source)
    end = time.time() + timeout
    while time.time() < end:
        same_name = uploads_dir / source.name
        if same_name.exists() and sha256(same_name) == source_hash:
            return same_name
        if uploads_dir.is_dir():
            for candidate in uploads_dir.iterdir():
                if (candidate.is_file()
                        and candidate.stat().st_mtime >= started_at - 2
                        and candidate.stat().st_size == source.stat().st_size
                        and sha256(candidate) == source_hash):
                    return candidate
        time.sleep(0.5)
    return None


def main():
    parser = argparse.ArgumentParser(description="Upload a file through the browser and verify it")
    parser.add_argument("--file", required=True, help="the file to upload")
    parser.add_argument("--uploads-dir", required=True, help="server folder where uploads land")
    parser.add_argument("--url", help="open this page first (optional)")
    parser.add_argument("--choose-image", help="screenshot of the 'Choose File' button")
    parser.add_argument("--choose-xy", nargs=2, type=int, metavar=("X", "Y"))
    parser.add_argument("--submit-image", help="screenshot of the Upload/Submit button")
    parser.add_argument("--submit-xy", nargs=2, type=int, metavar=("X", "Y"))
    parser.add_argument("--load-wait", type=float, default=3.0)
    parser.add_argument("--dialog-wait", type=float, default=2.0, help="seconds for the file dialog to open")
    args = parser.parse_args()

    source = Path(args.file).resolve()
    if not source.is_file():
        sys.exit(f"File not found: {source}")
    if not (args.choose_image or args.choose_xy):
        sys.exit("Give --choose-image or --choose-xy so the bot knows where 'Choose File' is.")

    print("Starting in 3s - don't touch the keyboard or mouse...")
    time.sleep(3)
    started_at = time.time()

    if args.url:
        webbrowser.open(args.url)
        time.sleep(args.load_wait)

    print("Clicking 'Choose File'...")
    if not click_target(args.choose_image, tuple(args.choose_xy) if args.choose_xy else None):
        sys.exit("FAIL: could not find the 'Choose File' button.")
    time.sleep(args.dialog_wait)

    print(f"Entering path in the dialog: {source}")
    paste_text(str(source))  # the file-name box has focus when the dialog opens
    pyautogui.press("enter")
    time.sleep(1.0)

    if args.submit_image or args.submit_xy:
        print("Clicking the submit button...")
        if not click_target(args.submit_image, tuple(args.submit_xy) if args.submit_xy else None):
            sys.exit("FAIL: could not find the submit button.")
    else:
        print("No submit button given - pressing Enter instead.")
        pyautogui.press("enter")

    print("Verifying the upload...")
    found = verify_upload(source, args.uploads_dir, started_at)
    if found:
        print(f"PASS: file arrived -> {found} ({found.stat().st_size} bytes)")
    else:
        pyautogui.screenshot("upload_failed.png")
        print(f"FAIL: '{source.name}' not found in {args.uploads_dir} (saved upload_failed.png)")
        sys.exit(1)


if __name__ == "__main__":
    main()
