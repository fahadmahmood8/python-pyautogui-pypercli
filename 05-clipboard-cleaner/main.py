"""Clipboard Cleaner
Copy messy text, strip extra spaces and line breaks in Python, paste it back clean.

Modes:
    python main.py            clean whatever is on the clipboard right now
    python main.py --auto     select text in any app, run this, and it copies,
                              cleans and pastes the clean text over the selection
    python main.py --paragraphs   keep blank-line paragraph breaks
"""
import argparse
import time

import pyautogui
import pyperclip

from cleaner import clean_text

pyautogui.FAILSAFE = True


def copy_selection(timeout=2.0):
    """Press Ctrl+C and wait until the clipboard actually changes."""
    pyperclip.copy("")  # clear first, so we can tell when the copy has landed
    pyautogui.hotkey("ctrl", "c")
    end = time.time() + timeout
    while time.time() < end:
        text = pyperclip.paste()
        if text:
            return text
        time.sleep(0.05)
    return ""


def main():
    parser = argparse.ArgumentParser(description="Clean messy clipboard text")
    parser.add_argument("--auto", action="store_true",
                        help="copy the current selection, clean it and paste it back")
    parser.add_argument("--paragraphs", action="store_true",
                        help="keep paragraph breaks (blank lines)")
    parser.add_argument("--delay", type=float, default=3,
                        help="seconds to wait in --auto mode so you can switch windows")
    args = parser.parse_args()

    if args.auto:
        print(f"Click into your app and SELECT the text. Starting in {args.delay:g}s...")
        time.sleep(args.delay)
        original = copy_selection()
        if not original:
            print("Nothing was copied - was any text selected?")
            return
    else:
        original = pyperclip.paste()
        if not original:
            print("The clipboard is empty.")
            return

    cleaned = clean_text(original, keep_paragraphs=args.paragraphs)
    pyperclip.copy(cleaned)

    print(f"Before: {len(original)} characters")
    print(f"After : {len(cleaned)} characters")
    print("-" * 40)
    print(cleaned[:300] + ("..." if len(cleaned) > 300 else ""))

    if args.auto:
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "v")
        print("Pasted the clean text back.")
    else:
        print("\nThe clean text is on your clipboard - just press Ctrl+V.")


if __name__ == "__main__":
    main()
