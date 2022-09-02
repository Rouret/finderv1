from src import fprint as fp
import sys
import subprocess
import os

class Finder:
    def __init__(self) -> None:
        self.name = "Finder"
        self.prompt_sign = ">>> "
        self.prompt = self.name + self.prompt_sign 
        self.commands = {
            "help": self.help,
            "quit": self._quit,
            "reload_dependencies": self.start,
            "wb_username": self.nexfil,
            "clear" : fp.fclear
        }
        self.vendor_folder = "vendor"
        self.output_folder = "output"

        self.python_exe = sys.executable
        
    def __setPrompt(self,routes = ""):
        self.prompt = self.name + "/" + "/".join(routes) + ">>> "


    def start(self):
        self.test()
        fp.fprint("Finder starter is starting ...", fp.YELLOW)
        #nexfil
        fp.fprint("nexfil https://github.com/thewhiteh4t/nexfil", fp.MAGENTA)
        self.__clone("nexfil","https://github.com/thewhiteh4t/nexfil.git", self.vendor_folder+"/nexfil")
        fp.fprint("Installing dependencies of nexfill ...", fp.MAGENTA)
        self.__pip_install(self.vendor_folder+"/nexfil/requirements.txt")
        fp.fprint("nexfil DONE", fp.GREEN)

        #END
        fp.fprint("\nFinder is ready to find u O_o\n", fp.YELLOW)
        
        
    def __clone(self,lib_name, url, folder):
        if(os.path.exists(folder)):
            fp.fprint(lib_name+" is already cloned", fp.GREEN)
        else:
            subprocess.run(["git", "clone", url, folder])

    def __pip_install(self, requirement_file):
       subprocess.run(["pip", "install", "-r", requirement_file], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            
    def nexfil(self):
        fp.fprint("The provided usernames are checked on over 350 websites within few seconds. (nexfil)", fp.YELLOW)
        options = ["username"]
        routes = ["nexfil"]
        self.__setPrompt(routes)
        self.__display_options(routes,options)
        result = self.__get_multiple_options(routes,options)
        if not result: return
        print("result: ", result)
        self.__setPrompt()
        
    def __display_options(self,routes,options):
        if len(routes) > 0:
            fp.fprint("\nOptions for " + routes[-1] + " :", fp.YELLOW)
        else: 
            fp.fprint("\nOptions:", fp.YELLOW)
        fp.fprint(",".join(options)+"\n", fp.YELLOW)

    def __get_multiple_options(self,routes,options):
        result = {}

        for option in options:
            temp_routes = routes
            temp_routes.append(option)
            self.__setPrompt(temp_routes)
            temp_input = ""
            while(len(temp_input) == 0):
                temp_input = input(self.prompt)
                if temp_input == "q": 
                    fp.fprint("Cancel wb_username", fp.RED)
                    self.__setPrompt()
                    return None
                if len(temp_input) == 0:
                    fp.fprint("Please provide a "+ option +" value !", fp.RED)
            result[option] = temp_input
        username = result["username"]
        routes.append(username)
        self.__setPrompt(routes)
        nexfill_folder = self.vendor_folder+"/nexfil"
        print(self.python_exe)
        subprocess.run([self.python_exe, "nexfil.py" , "-u", username ,"-f",self.output_folder+"/"+username+".txt"], cwd=os.path.abspath(nexfill_folder))
        fp.fprint("wb_username DONE for "+username + ", thanks to thewhiteh4t/nexfil", fp.GREEN)
        fp.fprint("Github: https://github.com/thewhiteh4t/nexfil\n", fp.GREEN)
        self.__setPrompt()
    

    def test(self):
        print(self.python_exe)
        return
        

    def help(self):
        for key in self.commands:
            fp.fprint( "- " + key, fp.GREEN)
    
 
    def _quit(self):
        fp.fprint("We will find u anyway à_à", fp.RED)
        sys.exit(0)