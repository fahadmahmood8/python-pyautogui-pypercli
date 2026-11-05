# 🪟 Window Organizer

**Level:** Intermediate

Launch Notepad and Calculator and tile them side by side automatically.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py            # add --swap to flip the sides
```

## What you'll practise

- Finding windows by title with PyGetWindow
- `moveTo()` / `resizeTo()` / `restore()`
- Using screen size to compute a layout

## Notes

- Windows only.
- `--taskbar 48` reserves space for the taskbar; adjust to your taskbar height.
- Calculator may enforce a minimum size, so it can look slightly different from Notepad.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
