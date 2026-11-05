# 🔁 Retry + Log Bot

**Level:** Advanced

Use the `@retry` decorator, structured logging and failure screenshots together.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## What you'll practise

- Writing a decorator with arguments (attempts, delay, backoff)
- Structured JSON-lines logging with rotation
- Capturing a screenshot on every failed attempt

## Notes

- Re-use it: `from main import retry, log` and decorate your own flaky steps.
- Logs: `logs/bot.jsonl`. Screenshots: `failures/`.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
