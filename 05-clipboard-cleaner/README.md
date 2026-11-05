# 📋 Clipboard Cleaner

**Level:** Intermediate

Copy messy text, strip extra spaces and line breaks in Python, paste it back clean.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py            # clean the clipboard
python main.py --auto     # select text in any app, then run: copy -> clean -> paste back
```

## What you'll practise

- `pyperclip.copy()` / `pyperclip.paste()`
- Regular expressions for whitespace cleanup
- Waiting for the clipboard to change after Ctrl+C
- Unit-testing the pure logic (`test_cleaner.py`)

## Notes

- `--paragraphs` keeps blank-line paragraph breaks.
- Run the tests: `python -m unittest` (no GUI needed).
- Cleaning logic lives in `cleaner.py` so it can be tested without PyAutoGUI.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `cleaner.py`
- `main.py`
- `test_cleaner.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
