"""LocalhostBot
A full Bot class: JSON config -> visit pages -> copy text -> screenshot -> HTML test report.

    python main.py                       # uses config.json
    python main.py --config my.json
"""
import argparse
import csv
import html
import json
import logging
import os
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

PHP_ERROR_RE = re.compile(
    r"Fatal error:|Parse error:|Warning:|Notice:|Deprecated:|Uncaught (?:Error|Exception)|Stack trace:",
    re.IGNORECASE)


class LocalhostBot:
    def __init__(self, config_path="config.json"):
        self.config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        self.base_url = self.config["base_url"].rstrip("/")
        self.load_wait = float(self.config.get("browser_wait", 3))
        self.shot_dir = Path(self.config.get("screenshot_dir", "output/screenshots"))
        self.report_dir = Path(self.config.get("report_dir", "output/reports"))
        self.shot_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.log = self._make_logger(self.config.get("log_file", "output/bot.log"))
        self.results = []

    # ------------------------------------------------------------------ setup
    @staticmethod
    def _make_logger(log_file):
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger("LocalhostBot")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", "%Y-%m-%d %H:%M:%S")
            for handler in (logging.StreamHandler(), logging.FileHandler(log_file, encoding="utf-8")):
                handler.setFormatter(fmt)
                logger.addHandler(handler)
        return logger

    # ------------------------------------------------------------------ actions
    def http_status(self, url, timeout=8):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            return exc.code
        except Exception:
            return 0

    def open_page(self, url):
        self.log.info("Opening %s", url)
        webbrowser.open_new_tab(url)
        time.sleep(self.load_wait)

    def copy_page_text(self, timeout=2.0):
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

    def screenshot(self, name):
        stamp = datetime.now().strftime("%H%M%S")
        safe = re.sub(r"[^A-Za-z0-9_-]+", "_", name)
        path = self.shot_dir / f"{safe}_{stamp}.png"
        pyautogui.screenshot(str(path))
        return path

    def close_tab(self):
        pyautogui.hotkey("ctrl", "w")

    # ------------------------------------------------------------------ test logic
    def check_page(self, page):
        name = page["name"]
        url = self.base_url + page["path"]
        expect = page.get("expect_text", "")
        started = time.time()
        problems = []

        status = self.http_status(url)
        self.open_page(url)
        text = self.copy_page_text()
        shot = self.screenshot(name)
        self.close_tab()

        if status == 0:
            problems.append("server unreachable")
        elif status >= 400:
            problems.append(f"HTTP {status}")
        if PHP_ERROR_RE.search(text):
            problems.append("PHP error text found on page")
        if expect and expect.lower() not in text.lower():
            problems.append(f"expected text missing: '{expect}'")
        if not text.strip() and status != 0:
            problems.append("page text is empty")

        result = {
            "name": name, "url": url, "http_status": status,
            "status": "FAIL" if problems else "PASS",
            "problems": "; ".join(problems),
            "seconds": round(time.time() - started, 1),
            "screenshot": str(shot),
        }
        (self.log.error if problems else self.log.info)("%s -> %s %s", name, result["status"], result["problems"])
        return result

    def run(self):
        self.log.info("Run started: %d pages", len(self.config["pages"]))
        for page in self.config["pages"]:
            try:
                self.results.append(self.check_page(page))
            except Exception as exc:
                self.log.exception("Unexpected error on %s", page.get("name"))
                self.results.append({"name": page.get("name", "?"), "url": self.base_url + page.get("path", ""),
                                     "http_status": 0, "status": "FAIL", "problems": f"bot error: {exc}",
                                     "seconds": 0, "screenshot": ""})
        report = self.write_html_report()
        self.write_csv()
        failed = sum(r["status"] == "FAIL" for r in self.results)
        self.log.info("Run finished: %d passed, %d failed. Report: %s",
                      len(self.results) - failed, failed, report)
        return failed

    # ------------------------------------------------------------------ reporting
    def write_csv(self):
        path = self.report_dir / "last_run.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.results[0].keys()))
            writer.writeheader()
            writer.writerows(self.results)

    def write_html_report(self):
        now = datetime.now()
        passed = sum(r["status"] == "PASS" for r in self.results)
        failed = len(self.results) - passed
        rows = []
        for r in self.results:
            color = "#16a34a" if r["status"] == "PASS" else "#dc2626"
            if r["screenshot"]:
                # path of the screenshot relative to the report file, so the HTML works anywhere
                rel = Path(os.path.relpath(r["screenshot"], self.report_dir)).as_posix()
                shot = f'<a href="{html.escape(rel)}"><img src="{html.escape(rel)}" width="160"></a>'
            else:
                shot = ""
            rows.append(
                f"<tr><td>{html.escape(r['name'])}</td>"
                f"<td><a href=\"{html.escape(r['url'])}\">{html.escape(r['url'])}</a></td>"
                f"<td>{r['http_status']}</td>"
                f"<td style=\"color:{color};font-weight:700\">{r['status']}</td>"
                f"<td>{html.escape(r['problems'])}</td><td>{r['seconds']}s</td><td>{shot}</td></tr>")
        doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>LocalhostBot report</title>
<style>
 body{{font-family:system-ui,sans-serif;margin:32px;color:#1f2937}}
 table{{border-collapse:collapse;width:100%}}
 th,td{{border:1px solid #e5e7eb;padding:8px;text-align:left;vertical-align:top;font-size:14px}}
 th{{background:#f3e8ff}}
 .sum span{{display:inline-block;margin-right:16px;padding:6px 12px;border-radius:6px;background:#f3f4f6}}
</style></head><body>
<h1>LocalhostBot test report</h1>
<p>{now:%Y-%m-%d %H:%M:%S}</p>
<p class="sum"><span>Total: {len(self.results)}</span><span style="color:#16a34a">Passed: {passed}</span><span style="color:#dc2626">Failed: {failed}</span></p>
<table><tr><th>Page</th><th>URL</th><th>HTTP</th><th>Result</th><th>Problems</th><th>Time</th><th>Screenshot</th></tr>
{''.join(rows)}
</table></body></html>"""
        path = self.report_dir / f"report_{now:%Y%m%d_%H%M%S}.html"
        path.write_text(doc, encoding="utf-8")
        (self.report_dir / "latest.html").write_text(doc, encoding="utf-8")
        return path


def main():
    parser = argparse.ArgumentParser(description="LocalhostBot - page tester with HTML report")
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()

    print("Starting in 3s - don't touch the keyboard or mouse...")
    time.sleep(3)
    failed = LocalhostBot(args.config).run()
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
