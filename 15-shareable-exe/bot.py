"""TeamBot - a tiny bot your teammates can run as a single .exe (no Python needed).

It reads config.json from the SAME FOLDER as the .exe, opens each page, takes a screenshot
and writes output/summary.txt. Build the exe with build.bat (or: python build.py).
"""
import json
import sys
import time
import webbrowser
from datetime import datetime
from pathlib import Path

import pyautogui

pyautogui.FAILSAFE = True


def app_dir():
    """Folder of the .exe when frozen by PyInstaller, otherwise the folder of this script."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def load_config():
    path = app_dir() / "config.json"
    if not path.exists():
        raise FileNotFoundError(f"config.json not found next to the program: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def run():
    config = load_config()
    out = app_dir() / "output"
    out.mkdir(exist_ok=True)
    wait = float(config.get("load_wait", 4))
    lines = [f"TeamBot run {datetime.now():%Y-%m-%d %H:%M:%S}", ""]

    print("TeamBot starting in 3 seconds - please don't touch the keyboard or mouse...")
    time.sleep(3)

    for i, url in enumerate(config["urls"], start=1):
        print(f"[{i}/{len(config['urls'])}] {url}")
        try:
            webbrowser.open_new_tab(url)
            time.sleep(wait)
            shot = out / f"page_{i:02d}_{datetime.now():%H%M%S}.png"
            pyautogui.screenshot(str(shot))
            pyautogui.hotkey("ctrl", "w")
            lines.append(f"OK    {url}  ->  {shot.name}")
        except Exception as exc:
            lines.append(f"ERROR {url}  ->  {exc}")

    (out / "summary.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nDone. See the 'output' folder next to the program: {out}")


def main():
    try:
        run()
    except Exception as exc:
        print(f"\nERROR: {exc}")
    finally:
        if getattr(sys, "frozen", False):
            input("\nPress Enter to close this window...")  # keeps the console open in the .exe


if __name__ == "__main__":
    main()
