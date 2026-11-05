# 🧪 WAMP Page Tester

**Level:** Advanced

Visit 5+ localhost URLs, copy the page text, detect PHP errors and write `report.csv`.

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

- Reading the page text via Ctrl+A / Ctrl+C
- Regex detection of `Fatal error`, `Warning`, `Notice`, `Parse error`...
- Combining an HTTP status check (urllib) with on-screen checks
- Writing a CSV report

## Notes

- Edit `urls.txt` to list your own pages.
- Verdicts: `OK`, `PHP_ERROR`, `HTTP_404`, `UNREACHABLE`, `EMPTY`.
- Your browser must be the default browser; keep it in the foreground while the bot runs.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `main.py`
- `urls.txt`

---
Part of the PyAutoGUI + Pyperclip practice projects.
