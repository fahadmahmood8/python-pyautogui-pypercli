# ⏰ Nightly Test Runner

**Level:** Professional

Schedule the bot to run at 02:30, test all pages, and alert you on failure.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run

```bash
python nightly_runner.py --run-once
python nightly_runner.py --install      # Windows Task Scheduler, daily 02:30
```

## What you'll practise

- Windows Task Scheduler via `schtasks`
- The `schedule` library for a long-running daemon
- Alerting by log file, e-mail (SMTP) and webhook

## Notes

- Uses HTTP checks (not PyAutoGUI) because a locked PC at 02:30 cannot be clicked.
- E-mail alerts: set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ALERT_FROM`, `ALERT_TO` environment variables.
- Webhook alerts: set `ALERT_WEBHOOK` to your Slack/Discord/Teams webhook URL. Never commit secrets to Git.
- Linux/macOS: use cron instead - `30 2 * * * python /path/nightly_runner.py --run-once`.
- Safety: PyAutoGUI's fail-safe is on - move the mouse into any screen corner to stop the bot immediately.
- Don't touch the keyboard or mouse while a bot is running; it controls them.

## Files

- `config.json`
- `nightly_runner.py`

---
Part of the PyAutoGUI + Pyperclip practice projects.
