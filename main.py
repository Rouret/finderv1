
import sys
import signal
import argparse
from zoneinfo import available_timezones
import pyreadline
from src.Finder import Finder
from src import fprint as fp
import collections
collections.Callable = collections.abc.Callable


def _quit():
	fp.fprint("We will find u anyway à_à", fp.RED)
	sys.exit(0)

finder = Finder()

#Commands frim commands folder
commands = {
	"help": finder.help,
	"exit": _quit,
	"quit": _quit,
	"q": _quit,
}


def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

#Parser config
parser = argparse.ArgumentParser(description='We will find u O_o')
args = parser.parse_args()

fp.fclear()
while(True):
	signal.signal(signal.SIGINT, _quit)
	pyreadline.Readline().parse_and_bind("tab: complete")
	pyreadline.Readline().set_completer(completer)

	cmd = input(": ")
	_cmd = commands.get(cmd)
	if(_cmd):
		_cmd()
	else:
		fp.fprint("Command not found", fp.RED)




