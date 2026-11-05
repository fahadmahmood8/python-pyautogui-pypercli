"""Nightly Test Runner
Tests every page in config.json at 02:30 and alerts you if anything fails.

Why HTTP checks instead of PyAutoGUI here? At 02:30 your PC is usually locked, and PyAutoGUI
cannot click on a locked screen. Plain HTTP checks keep working. (Use the Visual Regression /
LocalhostBot projects for on-screen checks while you are logged in.)

    python nightly_runner.py --run-once    run all tests now (what the scheduler calls)
    python nightly_runner.py --install     create a Windows Task Scheduler job, daily 02:30
    python nightly_runner.py --uninstall   remove that job
    python nightly_runner.py --daemon      stay open and run at 02:30 using the `schedule` library

Alerts (all optional, set as environment variables):
    SMTP_HOST, SMTP_PORT (587), SMTP_USER, SMTP_PASS, ALERT_FROM, ALERT_TO   -> e-mail
    ALERT_WEBHOOK                                                             -> Slack/Discord/Teams-style webhook
A line is always appended to logs/alerts.log.
"""
import argparse
import csv
import json
import os
import re
import smtplib
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG_DIR = HERE / "logs"
TASK_NAME = "NightlyTestRunner"
RUN_AT = "02:30"

PHP_ERROR_RE = re.compile(
    r"Fatal error:|Parse error:|Warning:|Notice:|Deprecated:|Uncaught (?:Error|Exception)|Stack trace:",
    re.IGNORECASE)


# --------------------------------------------------------------------------- testing
def check_url(page, timeout):
    url = page["url"]
    problems = []
    status, body, elapsed = 0, "", 0.0
    started = time.time()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            status = resp.status
            body = resp.read(300_000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        status = exc.code
        body = exc.read(300_000).decode("utf-8", errors="replace")
    except Exception as exc:
        problems.append(f"unreachable ({exc.__class__.__name__}: {exc})")
    elapsed = time.time() - started

    if status >= 400:
        problems.append(f"HTTP {status}")
    if PHP_ERROR_RE.search(body):
        problems.append("PHP error text in response")
    expect = page.get("expect_text", "")
    if expect and status and expect.lower() not in body.lower():
        problems.append(f"expected text missing: '{expect}'")
    slow = page.get("max_seconds")
    if slow and elapsed > slow:
        problems.append(f"slow: {elapsed:.1f}s > {slow}s")

    return {"name": page.get("name", url), "url": url, "http_status": status,
            "status": "FAIL" if problems else "PASS", "problems": "; ".join(problems),
            "seconds": round(elapsed, 2)}


def run_tests(config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    timeout = config.get("timeout_seconds", 10)
    results = [check_url(p, timeout) for p in config["pages"]]

    LOG_DIR.mkdir(exist_ok=True)
    out = LOG_DIR / f"nightly_{datetime.now():%Y%m%d_%H%M%S}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    failures = [r for r in results if r["status"] == "FAIL"]
    print(f"{len(results) - len(failures)} passed, {len(failures)} failed. Results: {out}")
    for r in failures:
        print(f"  FAIL {r['name']}: {r['problems']}")
    if failures:
        send_alerts(failures, len(results), out)
    return len(failures)


# --------------------------------------------------------------------------- alerts
def build_message(failures, total, csv_path):
    lines = [f"Nightly test run {datetime.now():%Y-%m-%d %H:%M}: {len(failures)} of {total} pages FAILED", ""]
    lines += [f"- {f['name']} ({f['url']}): {f['problems']}" for f in failures]
    lines += ["", f"Details: {csv_path}"]
    return "\n".join(lines)


def send_alerts(failures, total, csv_path):
    message = build_message(failures, total, csv_path)

    LOG_DIR.mkdir(exist_ok=True)
    with open(LOG_DIR / "alerts.log", "a", encoding="utf-8") as f:
        f.write(message + "\n" + "-" * 60 + "\n")
    print("Alert written to logs/alerts.log")

    host, to = os.environ.get("SMTP_HOST"), os.environ.get("ALERT_TO")
    if host and to:
        try:
            msg = EmailMessage()
            msg["Subject"] = f"[ALERT] {len(failures)} page(s) failing"
            msg["From"] = os.environ.get("ALERT_FROM", os.environ.get("SMTP_USER", "nightly-runner@localhost"))
            msg["To"] = to
            msg.set_content(message)
            with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=20) as smtp:
                smtp.starttls()
                if os.environ.get("SMTP_USER"):
                    smtp.login(os.environ["SMTP_USER"], os.environ.get("SMTP_PASS", ""))
                smtp.send_message(msg)
            print("E-mail alert sent.")
        except Exception as exc:
            print(f"E-mail alert failed: {exc}")

    hook = os.environ.get("ALERT_WEBHOOK")
    if hook:
        try:
            body = json.dumps({"text": message, "content": message}).encode("utf-8")
            req = urllib.request.Request(hook, data=body, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=15).close()
            print("Webhook alert sent.")
        except Exception as exc:
            print(f"Webhook alert failed: {exc}")


# --------------------------------------------------------------------------- scheduling
def install_task():
    if os.name != "nt":
        sys.exit("--install uses Windows Task Scheduler. On Linux/macOS add a cron line instead:\n"
                 f"  30 2 * * * {sys.executable} {HERE / 'nightly_runner.py'} --run-once")
    command = f'"{sys.executable}" "{HERE / "nightly_runner.py"}" --run-once'
    result = subprocess.run(["schtasks", "/Create", "/SC", "DAILY", "/TN", TASK_NAME,
                             "/TR", command, "/ST", RUN_AT, "/F"])
    if result.returncode == 0:
        print(f"Task '{TASK_NAME}' will run every day at {RUN_AT}.")
        print("Tip: in Task Scheduler tick 'Wake the computer to run this task' if it sleeps at night.")


def uninstall_task():
    subprocess.run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"])


def daemon(config_path):
    try:
        import schedule
    except ImportError:
        sys.exit("Install the scheduler library first:  pip install schedule")
    schedule.every().day.at(RUN_AT).do(run_tests, config_path)
    print(f"Waiting for {RUN_AT} every day. Keep this window open. Ctrl+C to quit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(20)
    except KeyboardInterrupt:
        print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description="Nightly page tester")
    parser.add_argument("--config", default=str(HERE / "config.json"))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run-once", action="store_true")
    group.add_argument("--install", action="store_true")
    group.add_argument("--uninstall", action="store_true")
    group.add_argument("--daemon", action="store_true")
    args = parser.parse_args()

    if args.run_once:
        sys.exit(1 if run_tests(args.config) else 0)
    elif args.install:
        install_task()
    elif args.uninstall:
        uninstall_task()
    elif args.daemon:
        daemon(args.config)


if __name__ == "__main__":
    main()
