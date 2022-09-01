import sys
import signal
import argparse
from src import printcolors as pc

def _quit():
	pc.printcolors("Bey World\n",pc.RED)
	sys.exit(0)

commands = {
'quit': _quit
}


_quit()




