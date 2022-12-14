import json
import sys
import signal
from src.Finder import Finder
from src import fprint as fp
import collections.abc

collections.Callable = collections.abc.Callable

is_windows = False
config_file = "config.json"
try:
    import gnureadline
except ImportError:
    is_windows = True
    import pyreadline


def _quit():
    fp.fprint(("We will find u anyway à_à", fp.RED))
    sys.exit(0)


config = json.load(open(config_file))
finder = Finder(config)

def completer(text, state):
    options = [i for i in finder.commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


signal.signal(signal.SIGINT, _quit)
if is_windows:
    pyreadline.Readline().parse_and_bind("tab: complete")
    pyreadline.Readline().set_completer(completer)
else:
    gnureadline.parse_and_bind("tab: complete")
    gnureadline.set_completer(completer)

fp.fclear(config["version"])
finder.start()
while True:
    cmd = input(finder.prompt)
    _cmd = finder.commands.get(cmd)
    if _cmd:
        _cmd["exec"]()
    else:
        fp.fprint(("Command not found", fp.RED))
