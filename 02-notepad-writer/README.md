# 📝 Notepad Writer

**Level:** Beginner

Open Notepad, paste a poem using `paste_text`, and save it with Ctrl+S.

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

- Launching an app with `subprocess.Popen`
- `paste_text()` = clipboard + Ctrl+V (fast, handles any character)
- Driving the Save As dialog

## Notes

- Windows only (uses `notepad.exe`).
- The poem is saved to `Documents/pyautogui_poems/` with a timestamped name.
- If the Save dialog is slow on your PC, raise the `time.sleep` values in `save_with_dialog()`.
- Fail-safe: slam the mouse into a screen corner to abort.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `main.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
