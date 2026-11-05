"""Build TeamBot.exe with PyInstaller and prepare a ready-to-share folder.

    pip install -r requirements.txt
    python build.py

Result: dist/TeamBot/  containing TeamBot.exe + config.json  (zip that folder and send it).
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = "TeamBot"


def main():
    cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--clean", "--noconfirm",
           "--name", NAME, "--distpath", str(HERE / "dist" / "_build"), str(HERE / "bot.py")]
    print("Running:", " ".join(cmd))
    if subprocess.run(cmd, cwd=HERE).returncode != 0:
        sys.exit("PyInstaller failed - see the messages above.")

    package = HERE / "dist" / NAME
    package.mkdir(parents=True, exist_ok=True)
    exe = next((HERE / "dist" / "_build").glob(f"{NAME}*"))
    shutil.copy2(exe, package / exe.name)
    shutil.copy2(HERE / "config.json", package / "config.json")  # editable by your team
    shutil.rmtree(HERE / "dist" / "_build", ignore_errors=True)

    print(f"\nDone! Share this folder: {package}")
    print("Teammates just double-click TeamBot.exe (edit config.json to change the pages).")


if __name__ == "__main__":
    main()
