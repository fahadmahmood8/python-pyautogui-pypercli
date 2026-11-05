# 🖱 Mouse Tracker

**Level:** Beginner · Module 2

Live-print the mouse coordinates and the RGB / HEX colour under the cursor. Ctrl+C stops it.

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

- `pyautogui.position()` and `pyautogui.pixel()`
- Rewriting one terminal line with `\r`
- Stopping a loop cleanly with `KeyboardInterrupt`

## Notes

- Use it to find the X/Y coordinates for the other projects (e.g. `--click`, `--choose-xy`).
- On multi-monitor or high-DPI setups the colour may show `n/a` at the very edge of the screen.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
