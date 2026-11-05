# 🎨 Paint Artist

**Level:** Beginner

Draw a square, a circle and a spiral in MS Paint using mouse drags.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py            # or: python main.py --size 300
```

## What you'll practise

- `mouseDown()` / `moveTo()` / `mouseUp()` to drag along a path
- Generating shapes with `math.sin` / `math.cos`
- Maximising a window with `win+up`

## Notes

- Windows only (uses `mspaint.exe`).
- Shapes are placed relative to your screen size, so they work on any resolution.
- Make sure the Pencil or Brush tool is selected (Paint's default).
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
