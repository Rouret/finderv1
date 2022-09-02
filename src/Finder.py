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
            "username": self.nexfil,
            "url": self.finalrecon,
            "clear" : fp.fclear
        }
        self.vendor_folder = "vendor"
        self.output_folder = "output"

        self.python_exe = sys.executable
        
    def start(self):
        self.test()
        fp.fprint("Finder starter is starting ...", fp.YELLOW)
        #nexfil
        self.__install_by_pip("nexfil","https://github.com/thewhiteh4t/nexfil")

        #FinalRecon
        if os.name == "nt":
            fp.fprint("FinalRecon is not supported on Windows", fp.RED)
        else:
            self.__install_by_pip("FinalRecon","https://github.com/thewhiteh4t/FinalRecon")
        #END
        fp.fprint("\nFinder is ready to find u O_o\n", fp.YELLOW)

    def __install_by_pip(self, lib_name, github_url):
        fp.fprint(lib_name + " " + github_url, fp.MAGENTA)
        self.__clone(lib_name, github_url+".git", self.vendor_folder+"/"+lib_name)
        fp.fprint("Installing dependencies of "+lib_name+" ...", fp.MAGENTA)
        self.__pip_install(self.vendor_folder+"/"+lib_name+"/requirements.txt")
        fp.fprint(lib_name+" DONE", fp.GREEN)

    def nexfil(self):
        fp.fprint("The provided usernames are checked on over 350 websites within few seconds. (nexfil)", fp.YELLOW)
        options = ["username"]
        routes = ["nexfil"]
        self.__setPrompt(routes)
        self.__display_options(routes,options)
        result = self.__get_multiple_options(routes,options)
        if not result: return
        username = result["username"]
        routes.append(username)
        self.__setPrompt(routes)
        nexfill_folder = self.vendor_folder+"/nexfil"
        subprocess.run([self.python_exe, "nexfil.py" , "-u", username], cwd=os.path.abspath(nexfill_folder))
        fp.fprint("wb_username DONE for "+username + ", thanks to thewhiteh4t/nexfil", fp.GREEN)
        fp.fprint("Github: https://github.com/thewhiteh4t/nexfil\n", fp.GREEN)
        self.__setPrompt()
        
    def finalrecon(self):
        if os.name == "nt":
            fp.fprint("FinalRecon is not supported on Windows", fp.RED)
            return
        fp.fprint("Goal of FinalRecon is to provide an overview of the target in a short amount of time while maintaining the accuracy of results. (FinalRecon)", fp.YELLOW)
        options = ["url"]
        routes = ["FinalRecon"]
        self.__setPrompt(routes)
        self.__display_options(routes,options)
        result = self.__get_multiple_options(routes,options)
        if not result: return
        url = result["url"]
        routes.append(url)
        self.__setPrompt(routes)
        finalrecon_folder = self.vendor_folder+"/FinalRecon"
        subprocess.run([self.python_exe, "finalrecon.py" , "--full", url], cwd=os.path.abspath(finalrecon_folder))
        fp.fprint("wb_username DONE for "+url + ", thanks to thewhiteh4t/FinalRecon", fp.GREEN)
        fp.fprint("Github: https://github.com/thewhiteh4t/FinalRecon\n", fp.GREEN)
        self.__setPrompt()
        
    def help(self):
        for key in self.commands:
            fp.fprint( "- " + key, fp.GREEN)

    def __setPrompt(self,routes = ""):
        self.prompt = self.name + "/" + "/".join(routes) + ">>> "

    def __clone(self,lib_name, url, folder):
        if(os.path.exists(folder)):
            fp.fprint(lib_name+" is already cloned", fp.GREEN)
        else:
            subprocess.run(["git", "clone", url, folder],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

    def __pip_install(self, requirement_file):
       subprocess.run(["pip", "install", "-r", requirement_file], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

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
        return result
    
    def test(self):
        print(self.python_exe)
        return
        
    def _quit(self):
        fp.fprint("We will find u anyway à_à", fp.RED)
        sys.exit(0)