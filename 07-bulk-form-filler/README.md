# 📂 Bulk Form Filler

**Level:** Intermediate

Read a CSV of people, fill a web form once per row, and screenshot each result.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py                       # uses the bundled demo_form.html + people.csv
python main.py --url http://localhost/contact.php --fields name,email,message --click 640 380
```

## What you'll practise

- `csv.DictReader`
- Filling fields with Tab + `paste_text`
- Per-row error handling and a `summary.csv`

## Notes

- The first form field must have focus: the demo uses `autofocus`; for other sites use `--click X Y`.
- `--fields` lists the CSV columns in the order the form is tabbed.
- Screenshots and `summary.csv` go to `results/`.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `demo_form.html`
- `main.py`
- `people.csv`

---
Part of the PyAutoGUI + Pyperclip practice projects.
