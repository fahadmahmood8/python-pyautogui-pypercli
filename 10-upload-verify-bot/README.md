# 📤 Upload + Verify Bot

**Level:** Advanced

Click "Choose File", upload via the native dialog, and verify the file exists in the `uploads/` folder.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python main.py --file sample_upload.txt --url http://localhost/upload-demo/ ^
    --choose-xy 600 350 --submit-xy 600 420 ^
    --uploads-dir C:\wamp64\www\upload-demo\uploads
```

## What you'll practise

- Typing a path into the native file dialog
- Locating buttons by image or by coordinates
- Verifying with a SHA-256 match (works even if the server renames the file)

## Notes

- Test it locally: copy the `demo/` folder to `C:\wamp64\www\upload-demo`.
- Find button coordinates with the Mouse Tracker project, or pass `--choose-image` / `--submit-image` screenshots.
- On failure the bot saves `upload_failed.png` and exits with code 1.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `demo/index.php`
- `main.py`
- `sample_upload.txt`

---
Part of the PyAutoGUI + Pyperclip practice projects.
