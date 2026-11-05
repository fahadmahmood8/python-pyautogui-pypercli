# 📦 Shareable .exe

**Level:** Professional

Package your bot with PyInstaller so your team can run it without Python.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
build.bat            # or: python build.py
```

## What you'll practise

- `pyinstaller --onefile`
- Finding files next to a frozen exe (`sys.frozen`)
- Shipping an editable `config.json` beside the exe

## Notes

- Output: `dist/TeamBot/` containing `TeamBot.exe` and `config.json` - zip that folder and share it.
- Build on Windows to get a Windows exe (PyInstaller does not cross-compile).
- Some antivirus tools flag unsigned PyInstaller exes; code-sign it or whitelist it for your team.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `bot.py`
- `build.bat`
- `build.py`
- `config.json`

---
Part of the PyAutoGUI + Pyperclip practice projects.
