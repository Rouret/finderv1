from src import fprint as fp


class Finder:
    def __init__(self) -> None:
        self.name = "Finder"

    
    def help(self):
        fp.fprint("help", fp.BLUE)