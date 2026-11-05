# 🔍 Visual Regression

**Level:** Advanced

Save a baseline screenshot and compare daily screenshots against it with `ImageChops`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py baseline --delay 5
python main.py compare --max-diff 0.5
```

## What you'll practise

- `PIL.ImageChops.difference()`
- Ignoring tiny rendering noise with a tolerance
- Highlighting changed pixels in red
- Exit codes (0 = pass, 1 = fail) for automation

## Notes

- Use the same `--region` for baseline and compare so the image sizes match.
- Diff images are saved in `diffs/`, captures in `captures/`.
- Run `compare` daily with Windows Task Scheduler (see the Nightly Test Runner project).
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
