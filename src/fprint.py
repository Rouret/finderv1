from src import logo
import os
import sys

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def has_colours(stream):
    if not (hasattr(stream, "isatty") and stream.isatty):
        return False
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except Exception:
        return False


def fprint(*args):
    if has_colours:
        seq = ""
        for (text, color) in args:
            seq += "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m"
        sys.stdout.write(seq + "\n")
    else:
        text = ""
        for (text, color) in args:
            text += text
        sys.stdout.write(text)


def fclear():
    os.system('cls' if os.name == 'nt' else 'clear')
    fprint((logo.ascii_logo, WHITE))
    fprint(("Version: ", GREEN), ("V0.0.1", YELLOW),(" We will find u O_o", WHITE))
