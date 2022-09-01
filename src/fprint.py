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
    except:
        return False

def fprint(text, color=WHITE):
    if has_colours:
        seq = "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m"
        sys.stdout.write(seq)
    else:
        sys.stdout.write(text)

def fclear():
    #exec cls for window and clear for linux
    os.system('cls' if os.name == 'nt' else 'clear')
    return fprint(logo.ascii_logo,WHITE)
    

