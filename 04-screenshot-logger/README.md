# 📸 Screenshot Logger

**Level:** Beginner

Take a screenshot every 30 seconds with a timestamped file name.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py --interval 30
```

## What you'll practise

- `pyautogui.screenshot(path)`
- Timestamps with `datetime.strftime`
- A drift-free timing loop with `time.monotonic()`

## Notes

- Options: `--interval`, `--count` (0 = forever), `--folder`.
- Files are saved as `screenshots/screenshot_YYYY-MM-DD_HH-MM-SS.png`.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
