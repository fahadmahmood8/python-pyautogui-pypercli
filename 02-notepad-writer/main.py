"""Notepad Writer
Opens Notepad, pastes a poem with paste_text() and saves it with Ctrl+S.
Move the mouse to a screen corner to trigger the PyAutoGUI fail-safe and abort.
"""
import subprocess
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

POEM = """The Cursor's Lullaby

A little arrow wakes at dawn,
It glides across the glowing lawn,
It clicks the doors that stay shut tight
And types a poem in the night.

No hands were needed, no one's there,
Just Python dancing through the air,
Copy, paste, and save with grace -
Automation finds its place.
"""

SAVE_FOLDER = Path.home() / "Documents" / "pyautogui_poems"


def paste_text(text, pause=0.15):
    """Put text on the clipboard and paste it (fast and handles any characters)."""
    pyperclip.copy(text)
    time.sleep(pause)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(pause)


def open_notepad():
    subprocess.Popen(["notepad.exe"])
    time.sleep(2.0)  # give Notepad time to appear and take focus


def save_with_dialog(path):
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1.2)  # wait for the Save As dialog
    paste_text(str(path))  # the file-name box is focused by default
    pyautogui.press("enter")
    time.sleep(1.0)


def main():
    SAVE_FOLDER.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = SAVE_FOLDER / f"poem_{stamp}.txt"

    print("Starting in 3 seconds - don't touch the keyboard or mouse...")
    time.sleep(3)

    open_notepad()
    paste_text(POEM)
    save_with_dialog(target)

    if target.exists():
        print(f"Saved: {target}")
    else:
        print("The file was not found - the Save dialog may have looked different.")
        print("Tip: increase the sleep times in save_with_dialog().")


if __name__ == "__main__":
    main()
