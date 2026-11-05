"""Bulk Form Filler
Reads people.csv and fills a web form once per row, taking a screenshot of each result.

The form is filled with the Tab key, so the first field must have focus after the page loads.
(The bundled demo_form.html uses `autofocus`. For another site use --click X Y to click
 into the first field first - find the coordinates with the Mouse Tracker project.)

Examples:
    python main.py
    python main.py --url http://localhost/contact.php --fields name,email,message --click 640 380
"""
import argparse
import csv
import re
import time
import webbrowser
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15

HERE = Path(__file__).resolve().parent


def paste_text(text, pause=0.12):
    pyperclip.copy(text)
    time.sleep(pause)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(pause)


def slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "row"


def load_rows(csv_path):
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def go_to(url, first):
    if first:
        webbrowser.open(url)
    else:
        pyautogui.hotkey("ctrl", "l")  # focus the address bar of the active browser tab
        paste_text(url)
        pyautogui.press("enter")


def fill_form(row, fields, click_xy):
    if click_xy:
        pyautogui.click(*click_xy)
        time.sleep(0.2)
    for i, field in enumerate(fields):
        paste_text(row.get(field, ""))
        if i < len(fields) - 1:
            pyautogui.press("tab")


def main():
    parser = argparse.ArgumentParser(description="Fill a web form from a CSV file")
    parser.add_argument("--csv", default=str(HERE / "people.csv"))
    parser.add_argument("--url", default=(HERE / "demo_form.html").as_uri())
    parser.add_argument("--fields", default="name,email,phone,message",
                        help="CSV columns, in the order the form fields are tabbed")
    parser.add_argument("--click", nargs=2, type=int, metavar=("X", "Y"),
                        help="click here before filling (focus the first field)")
    parser.add_argument("--load-wait", type=float, default=3.0, help="seconds for the page to load")
    parser.add_argument("--result-wait", type=float, default=1.5, help="seconds to wait after submitting")
    parser.add_argument("--out", default="results", help="folder for screenshots + summary.csv")
    args = parser.parse_args()

    fields = [f.strip() for f in args.fields.split(",") if f.strip()]
    rows = load_rows(args.csv)
    if not rows:
        print("The CSV has no rows.")
        return

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    summary = []

    print(f"{len(rows)} rows to submit. Starting in 3s - don't touch the keyboard or mouse...")
    time.sleep(3)

    for index, row in enumerate(rows, start=1):
        label = row.get(fields[0], f"row{index}")
        print(f"[{index}/{len(rows)}] {label}")
        status, shot = "submitted", ""
        try:
            go_to(args.url, first=(index == 1))
            time.sleep(args.load_wait)
            fill_form(row, fields, tuple(args.click) if args.click else None)
            pyautogui.press("enter")  # submit
            time.sleep(args.result_wait)
            shot = out / f"{index:03d}_{slugify(label)}.png"
            pyautogui.screenshot(str(shot))
        except Exception as exc:  # keep going if one row fails
            status = f"error: {exc}"
            print(f"   !! {status}")
        summary.append({"row": index, "name": label, "status": status,
                        "screenshot": str(shot),
                        "time": datetime.now().isoformat(timespec="seconds")})

    with open(out / "summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["row", "name", "status", "screenshot", "time"])
        writer.writeheader()
        writer.writerows(summary)
    print(f"Done. Screenshots and summary.csv are in '{out}'.")


if __name__ == "__main__":
    main()
