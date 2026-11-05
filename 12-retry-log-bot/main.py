"""Retry + Log Bot
Shows the three reliability tools working together:
  * an @retry decorator (attempts, delay, exponential backoff)
  * structured logging (readable console + JSON-lines file with rotation)
  * a failure screenshot saved on every failed attempt

Run the demo:   python main.py
Then inspect:   logs/bot.jsonl   and   failures/*.png
"""
import functools
import json
import logging
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pyautogui

pyautogui.FAILSAFE = True

LOG_DIR = Path("logs")
FAIL_DIR = Path("failures")
EXTRA_KEYS = ("step", "attempt", "max_attempts", "error", "screenshot")


class JsonFormatter(logging.Formatter):
    """One JSON object per line - easy to grep, load into pandas or ship to a log service."""

    def format(self, record):
        payload = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        for key in EXTRA_KEYS:
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger("bot")
    if logger.handlers:  # already configured
        return logger
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s %(message)s", "%H:%M:%S"))

    file_handler = RotatingFileHandler(LOG_DIR / "bot.jsonl", maxBytes=1_000_000,
                                       backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JsonFormatter())

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger


log = setup_logging()


def failure_screenshot(step, attempt):
    """Save the screen as evidence. Never raises - a failing screenshot must not hide the real error."""
    try:
        FAIL_DIR.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = FAIL_DIR / f"{stamp}_{step}_attempt{attempt}.png"
        pyautogui.screenshot(str(path))
        return str(path)
    except Exception:
        return None


def retry(attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,), screenshot=True):
    """Retry a flaky step. Waits `delay` seconds, multiplied by `backoff` after each failure."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, attempts + 1):
                ctx = {"step": func.__name__, "attempt": attempt, "max_attempts": attempts}
                log.info("starting step", extra=ctx)
                try:
                    result = func(*args, **kwargs)
                except exceptions as exc:
                    shot = failure_screenshot(func.__name__, attempt) if screenshot else None
                    log.warning("attempt failed", extra={**ctx, "error": repr(exc), "screenshot": shot})
                    if attempt == attempts:
                        log.error("giving up", extra={**ctx, "error": repr(exc)})
                        raise
                    log.info(f"retrying in {wait:g}s", extra=ctx)
                    time.sleep(wait)
                    wait *= backoff
                else:
                    log.info("step succeeded", extra=ctx)
                    return result

        return wrapper

    return decorator


# ----------------------------------------------------------------------------- demo steps
_calls = {"count": 0}


@retry(attempts=4, delay=0.5, backoff=2)
def flaky_click():
    """Pretends to click something that only works on the 3rd try."""
    _calls["count"] += 1
    if _calls["count"] < 3:
        raise RuntimeError(f"button not ready (call #{_calls['count']})")
    return "clicked"


@retry(attempts=2, delay=0.3)
def always_fails():
    raise TimeoutError("the page never loaded")


def main():
    log.info("=== demo 1: flaky step that recovers ===")
    print("Result:", flaky_click())

    log.info("=== demo 2: step that never works ===")
    try:
        always_fails()
    except TimeoutError:
        log.error("demo 2 failed as expected - see failures/ for the screenshots")

    print("\nDone. Open logs/bot.jsonl and the failures/ folder to see what was recorded.")


if __name__ == "__main__":
    main()
