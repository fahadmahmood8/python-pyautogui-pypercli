# 🧩 Playwright + PyAutoGUI

**Level:** Professional

Use Playwright for page DOM checks and PyAutoGUI for file dialogs and desktop actions.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
playwright install chromium
python main.py
```

## What you'll practise

- DOM assertions with `playwright.sync_api.expect`
- Why native OS dialogs need PyAutoGUI
- Handing control back and forth between the two tools

## Notes

- The browser runs headed (visible) - a native dialog cannot appear in headless mode.
- Playwright can also handle file choosers itself with `page.expect_file_chooser()`; this demo shows the PyAutoGUI route for dialogs Playwright can't reach.
- Screenshots land in `output/`.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `demo_page.html`
- `main.py`
- `sample_upload.txt`

---
Part of the PyAutoGUI + Pyperclip practice projects.
