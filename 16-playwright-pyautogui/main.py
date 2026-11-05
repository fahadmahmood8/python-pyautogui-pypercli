"""Playwright + PyAutoGUI
Playwright is great at the page DOM (title, elements, text) but cannot drive a native OS file
dialog. PyAutoGUI can. This demo uses each for what it does best:

  1. Playwright : open the page, assert title / button / heading in the DOM
  2. Playwright : click the file input  (the real OS dialog opens)
  3. PyAutoGUI  : paste the file path into the native dialog and press Enter
  4. Playwright : assert the page now shows the chosen file name
  5. PyAutoGUI  : take a full-desktop screenshot as extra evidence

    pip install -r requirements.txt
    playwright install chromium
    python main.py
"""
import time
from pathlib import Path

import pyautogui
import pyperclip
from playwright.sync_api import expect, sync_playwright

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

HERE = Path(__file__).resolve().parent
PAGE = (HERE / "demo_page.html").as_uri()
FILE_TO_UPLOAD = HERE / "sample_upload.txt"
OUT = HERE / "output"


def paste_text(text, pause=0.15):
    pyperclip.copy(text)
    time.sleep(pause)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(pause)


def main():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # a visible window is needed for the OS dialog
        page = browser.new_page()
        try:
            # 1. DOM checks with Playwright --------------------------------------------------
            page.goto(PAGE)
            expect(page).to_have_title("Playwright + PyAutoGUI Demo")
            expect(page.locator("h1")).to_have_text("Upload a file")
            expect(page.locator("#file-input")).to_be_visible()
            print("DOM checks passed (title, heading, file input).")

            # 2. Open the native file dialog --------------------------------------------------
            page.bring_to_front()
            page.click("#file-input", no_wait_after=True)
            time.sleep(2.0)  # let the OS dialog appear

            # 3. Drive the native dialog with PyAutoGUI ---------------------------------------
            paste_text(str(FILE_TO_UPLOAD))
            pyautogui.press("enter")
            time.sleep(1.0)

            # 4. Back to Playwright: did the page see the file? -------------------------------
            expect(page.locator("#filename")).to_have_text(FILE_TO_UPLOAD.name, timeout=5000)
            print(f"Page shows the selected file: {FILE_TO_UPLOAD.name}")

            # 5. Evidence: page screenshot (Playwright) + desktop screenshot (PyAutoGUI) -------
            page.screenshot(path=str(OUT / "page.png"))
            pyautogui.screenshot(str(OUT / "desktop.png"))
            print(f"PASS - screenshots saved in {OUT}")
        except Exception as exc:
            print(f"FAIL: {exc}")
            pyautogui.screenshot(str(OUT / "failure_desktop.png"))
            raise
        finally:
            time.sleep(1)
            browser.close()


if __name__ == "__main__":
    main()
