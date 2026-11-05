# 🤖 LocalhostBot Class

**Level:** Professional · Module 15

A full `Bot` class with JSON config, logging and an HTML test report.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py --config config.json
```

## What you'll practise

- Structuring automation as a class
- JSON-driven configuration
- Generating an HTML report with screenshots
- Meaningful exit codes

## Notes

- Edit `config.json` to define your pages and the text each should contain.
- Open `output/reports/latest.html` after a run.
- Exit code is 1 when any page fails.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `config.json`
- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
