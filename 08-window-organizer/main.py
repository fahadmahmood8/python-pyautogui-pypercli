"""Window Organizer
Launches Notepad and Calculator and tiles them side by side automatically (Windows).
"""
import argparse
import subprocess
import time

import pyautogui
import pygetwindow as gw


def wait_for_window(keyword, timeout=15):
    """Return the first visible window whose title contains `keyword`."""
    end = time.time() + timeout
    keyword = keyword.lower()
    while time.time() < end:
        for win in gw.getAllWindows():
            if win.title.strip() and keyword in win.title.lower():
                return win
        time.sleep(0.3)
    return None


def place(win, left, top, width, height):
    if win.isMinimized or win.isMaximized:
        win.restore()
        time.sleep(0.3)
    win.moveTo(left, top)
    win.resizeTo(width, height)


def main():
    parser = argparse.ArgumentParser(description="Tile Notepad and Calculator side by side")
    parser.add_argument("--taskbar", type=int, default=48, help="taskbar height in pixels to leave free")
    parser.add_argument("--swap", action="store_true", help="Calculator on the left, Notepad on the right")
    args = parser.parse_args()

    screen_w, screen_h = pyautogui.size()
    usable_h = screen_h - args.taskbar
    half_w = screen_w // 2

    print("Launching Notepad and Calculator...")
    subprocess.Popen(["notepad.exe"])
    subprocess.Popen(["calc.exe"])

    notepad = wait_for_window("notepad")
    calc = wait_for_window("calculator")
    if not notepad or not calc:
        print(f"Could not find: {'Notepad ' if not notepad else ''}{'Calculator' if not calc else ''}")
        return

    left_win, right_win = (calc, notepad) if args.swap else (notepad, calc)
    place(left_win, 0, 0, half_w, usable_h)
    place(right_win, half_w, 0, half_w, usable_h)
    print(f"Tiled: '{left_win.title}' (left)  |  '{right_win.title}' (right)")

    # Bonus: type something into Notepad to prove it is the active, writable window.
    notepad.activate()


if __name__ == "__main__":
    main()
