"""WAMP Page Tester
Visits 5+ localhost URLs in your browser, copies the visible page text, detects PHP errors
and writes report.csv.

Edit urls.txt (one URL per line, '#' for comments), then:   python main.py
"""
import argparse
import csv
import re
import time
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

HERE = Path(__file__).resolve().parent

# Typical PHP error / warning signatures as they appear in rendered page text.
PHP_ERROR_PATTERNS = [
    r"Fatal error:",
    r"Parse error:",
    r"Warning:",
    r"Notice:",
    r"Deprecated:",
    r"Uncaught (?:Error|Exception|TypeError|ArgumentCountError)",
    r"Stack trace:",
    r"Call to undefined (?:function|method)",
]
PHP_ERROR_RE = re.compile("|".join(PHP_ERROR_PATTERNS), re.IGNORECASE)


def load_urls(path):
    urls = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def find_php_errors(text):
    """Return a list of the lines containing PHP error signatures."""
    return [line.strip()[:160] for line in text.splitlines() if PHP_ERROR_RE.search(line)]


def http_status(url, timeout=8):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:
        return 0  # server down / refused


def copy_page_text(timeout=2.0):
    pyperclip.copy("")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "c")
    end = time.time() + timeout
    while time.time() < end:
        text = pyperclip.paste()
        if text:
            return text
        time.sleep(0.05)
    return ""


def main():
    parser = argparse.ArgumentParser(description="Visit localhost pages and report PHP errors")
    parser.add_argument("--urls", default=str(HERE / "urls.txt"))
    parser.add_argument("--load-wait", type=float, default=3.0, help="seconds for each page to load")
    parser.add_argument("--report", default="report.csv")
    args = parser.parse_args()

    urls = load_urls(args.urls)
    if not urls:
        print("No URLs found in", args.urls)
        return

    print(f"Testing {len(urls)} pages. Starting in 3s - don't touch the keyboard or mouse...")
    time.sleep(3)

    rows = []
    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] {url}")
        status = http_status(url)
        webbrowser.open_new_tab(url)
        time.sleep(args.load_wait)
        text = copy_page_text()
        errors = find_php_errors(text)
        pyautogui.hotkey("ctrl", "w")  # close the tab again

        if status == 0:
            verdict = "UNREACHABLE"
        elif status >= 400:
            verdict = f"HTTP_{status}"
        elif errors:
            verdict = "PHP_ERROR"
        elif not text.strip():
            verdict = "EMPTY"
        else:
            verdict = "OK"

        first_line = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")[:100]
        rows.append({
            "time": datetime.now().isoformat(timespec="seconds"),
            "url": url,
            "http_status": status,
            "verdict": verdict,
            "text_length": len(text),
            "php_errors": " | ".join(errors),
            "first_line": first_line,
        })
        print(f"      -> {verdict}")
        time.sleep(0.5)

    with open(args.report, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    bad = [r for r in rows if r["verdict"] != "OK"]
    print(f"\nReport written to {args.report}: {len(rows) - len(bad)} OK, {len(bad)} with problems.")


if __name__ == "__main__":
    main()
