# 🖼 Image-Click Bot

**Level:** Intermediate

Capture a button image, wait for it to appear, click it, repeat.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python capture_template.py --name button
python main.py templates/button.png --repeat 5
```

## What you'll practise

- `locateCenterOnScreen()` with `confidence`
- Polling with a timeout
- Waiting for the button to disappear so you never double-click

## Notes

- `confidence=` needs OpenCV, which is included in `requirements.txt`.
- Lower `--confidence` (e.g. 0.75) if the button is not found; raise it if the wrong thing gets clicked.
- Capture the template at the same screen scaling (DPI) you will run at.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `capture_template.py`
- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
