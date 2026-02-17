#!/usr/bin/env python3
"""Auto CMD+Tab sender with TUI control."""

import curses
import subprocess
import time


def send_cmd_tab():
    subprocess.run(
        ["osascript", "-e", 'tell application "System Events" to key code 48 using command down'],
        capture_output=True,
    )


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    interval = 1.0
    paused = True
    last_send = 0
    send_count = 0

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_CYAN, -1)

    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        # Title
        title = " CMD+Tab Auto Sender "
        stdscr.addstr(1, max(0, (width - len(title)) // 2), title, curses.A_BOLD | curses.color_pair(4))
        stdscr.addstr(2, max(0, (width - len(title)) // 2), "=" * len(title), curses.color_pair(4))

        # Status
        if paused:
            status = "|| PAUSED"
            color = curses.color_pair(2)
        else:
            status = ">> RUNNING"
            color = curses.color_pair(1)
        stdscr.addstr(4, 4, "Status:   ", curses.A_BOLD)
        stdscr.addstr(status, color | curses.A_BOLD)

        # Interval
        stdscr.addstr(5, 4, "Interval: ", curses.A_BOLD)
        stdscr.addstr(f"{interval:.1f}s", curses.color_pair(3) | curses.A_BOLD)

        # Send count
        stdscr.addstr(6, 4, "Sent:     ", curses.A_BOLD)
        stdscr.addstr(str(send_count), curses.color_pair(3) | curses.A_BOLD)

        # Divider
        stdscr.addstr(8, 4, "Controls", curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(9, 4, "[Space]    Pause / Resume")
        stdscr.addstr(10, 4, "[Up / +]   Interval +0.5s")
        stdscr.addstr(11, 4, "[Down / -] Interval -0.5s")
        stdscr.addstr(12, 4, "[r]        Reset counter")
        stdscr.addstr(13, 4, "[q]        Quit")

        stdscr.refresh()

        # Input
        try:
            key = stdscr.getch()
        except Exception:
            key = -1

        if key in (ord("q"), ord("Q")):
            break
        elif key == ord(" "):
            paused = not paused
            if not paused:
                last_send = time.time()
        elif key in (curses.KEY_UP, ord("+"), ord("=")):
            interval = min(interval + 0.5, 60.0)
        elif key in (curses.KEY_DOWN, ord("-")):
            interval = max(interval - 0.5, 0.5)
        elif key in (ord("r"), ord("R")):
            send_count = 0

        # Send if running and interval elapsed
        if not paused:
            now = time.time()
            if now - last_send >= interval:
                send_cmd_tab()
                send_count += 1
                last_send = now


if __name__ == "__main__":
    curses.wrapper(main)
