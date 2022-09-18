import asyncio
from urllib import request
from src import fprint as fp
from src.UsernameGenerator import UsernameGenerator
import sys
import subprocess
import os
from datetime import datetime
import requests
import codecs

requests.packages.urllib3.disable_warnings()


class Finder:
    def __init__(self, config) -> None:
        self.config = config
        self.name = "Finder"
        self.prompt_sign = "> "
        self.prompt = ""
        self.__set_prompt()
        self.commands = {
            "help": {
                "description": "Display this help",
                "exec": self.help
            },
            "username": {
                "description": "Find username on over 350 websites (by nexfil)",
                "exec": self.nexfil
            },
            "url": {
                "description": "Find information about a website (by FinalRecon)",
                "exec": self.finalrecon
            },
            "fsearch": {
                "description": "Find user ig account by firstname/lastname (by Finder)",
                "exec": self.fsearch
            },
            "fig":{
                "description": "Find location/hobbies/friends of an ig account (by Finder)",
                "exec": self.finder_ig
            },
            "update": {
                "description": "Update Finder",
                "exec": self.update
            },
            "clear": {
                "description": "Clear the screen",
                "exec": fp.fclear
            },
            "quit": {
                "description": "Quit Finder",
                "exec": self._quit
            },
            "reload_dependencies": {
                "description": "Reload dependencies",
                "exec": self.start
            },
        }
        self.vendor_folder = "vendor"
        self.output_folder = "output"

        self.python_exe = sys.executable
        self.test()

    def start(self):
        fp.fprint(("Finder starter is starting ...", fp.YELLOW))
        # nexfil
        self.__install_by_pip("nexfil", "https://github.com/thewhiteh4t/nexfil")

        # FinalRecon
        if os.name == "nt":
            fp.fprint(("FinalRecon is not supported on Windows", fp.RED))
        else:
            self.__install_by_pip("FinalRecon", "https://github.com/thewhiteh4t/FinalRecon")
        # END
        fp.fprint(("\nFinder is ready to find u O_o\n", fp.YELLOW))

    def update(self):
        fp.fprint(("Updating ...", fp.YELLOW))
        subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        self.__pip_install("requirements.txt")
        fp.fprint((f'Update DONE:\'{self.python_exe} {os.path.abspath(__file__)}\'', fp.GREEN))
        self._quit()

    def nexfil(self):
        fp.fclear(self.config["version"])
        fp.fprint((self.commands["username"]["description"], fp.YELLOW))
        options = ["username"]
        lib_name = "nexfil"
        self.__display_options(lib_name, options)
        result = self.__get_multiple_options(lib_name, options)
        if not result: return
        username = result["username"]
        nexfill_folder = self.vendor_folder + "/nexfil"
        subprocess.run([self.python_exe, "nexfil.py", "-u", username], cwd=os.path.abspath(nexfill_folder))
        fp.fprint(("username DONE for " + username + ", thanks to thewhiteh4t/nexfil", fp.GREEN))
        fp.fprint(("Github: https://github.com/thewhiteh4t/nexfil\n", fp.GREEN))
        self.__set_prompt()

    def finalrecon(self):
        if os.name == "nt":
            fp.fprint(("FinalRecon is not supported on Windows", fp.RED))
            return
        fp.fclear(self.config["version"])
        fp.fprint((self.commands["url"]["description"], fp.YELLOW))
        options = ["url"]
        lib_name = "FinalRecon"
        self.__display_options(lib_name, options)
        result = self.__get_multiple_options(lib_name, options)
        if not result: return
        url = result["url"]
        finalrecon_folder = self.vendor_folder + "/FinalRecon"
        subprocess.run([self.python_exe, "finalrecon.py", "--full", url], cwd=os.path.abspath(finalrecon_folder))
        fp.fprint(("wb_username DONE for " + url + ", thanks to thewhiteh4t/FinalRecon", fp.GREEN))
        fp.fprint(("Github: https://github.com/thewhiteh4t/FinalRecon\n", fp.GREEN))
        self.__set_prompt()

    def finder_ig(self):
        if not self.__check_ig_session_id():
            return
        fp.fclear(self.config["version"])
        fp.fprint((self.commands["fig"]["description"], fp.YELLOW))
        options = ["username"]
        lib_name = "fig"
        self.__display_options(lib_name, options)
        result = self.__get_multiple_options(lib_name, options)
        if not result: return
        username = result["username"]

       
        response = self.__get_instagram_graph(username)
        res_json = response.json()

        if "data" not in res_json:
            fp.fprint(("Error account exist ?", fp.RED))
            return

        SEO = ", ".join(map(lambda t: t[0], res_json["seo_category_infos"]))
        BIO = res_json["graphql"]["user"]["biography"]
        media = res_json["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

        fp.fprint((username, fp.YELLOW),(" profile is loaded", fp.GREEN))
        #SEO categories
        fp.fprint(("SEO: ", fp.YELLOW),(SEO, fp.GREEN))
        fp.fprint(("BIO: ", fp.YELLOW),(BIO, fp.GREEN))

       
        fp.fprint(("Nb of media: ", fp.YELLOW),(str(len(media)), fp.GREEN))
        #Check if there are some mention in the description
        users = []

        def add_user(username):
            i = 0
            isFind = False
            while i < len(users) and not isFind:
                if users[i]["username"] == username:
                    isFind = True
                i += 1
            if not isFind:
                users.append({"username": username, "nb": 1})
            else:
                users[i-1]["nb"] += 1
        for m in media:
            if m["node"]["edge_media_to_caption"]["edges"]:
                caption = m["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]

                caption_splited = caption.split("@")

                for i in range(1,len(caption_splited)):
                    mention = caption_splited[i].split(" ")[0]
                    add_user(mention)

            if m["node"]["edge_media_to_tagged_user"]["edges"]:
                for tag in m["node"]["edge_media_to_tagged_user"]["edges"]:
                    add_user(tag["node"]["user"]["username"])
            
        #sort users by nb
        users.sort(key=lambda u: u["nb"], reverse=True)
        
        fp.fprint(("Mentioned users: ", fp.YELLOW))
        for user in users:
            fp.fprint(("+ ",fp.GREEN),(user["username"], fp.YELLOW),(" : ", fp.YELLOW),(str(user["nb"]), fp.GREEN))


        #write result on a file
        filename = self.output_folder + "/result_fig_" + str(datetime.timestamp(datetime.now())) + "_" + username + ".txt"

        file = codecs.open(filename, "w", "utf-8")

        file_content = "SEO: " + SEO + "\n"
        file_content += "BIO: " + BIO + "\n"
        file_content +="Nb of media: " + str(len(media)) + "\n"
        file_content += "Mentioned users: \n"
        for user in users:
            file_content += "+ " + user["username"] + " : " + str(user["nb"]) + "\n"

        file.write(file_content)
        file.close()
        
        fp.fprint(("Result saved in ", fp.YELLOW),(filename, fp.GREEN))
    
        self.__set_prompt()


    def fsearch(self):
        if not self.__check_ig_session_id():
            return

        fp.fclear(self.config["version"])
        fp.fprint((self.commands["fsearch"]["description"], fp.YELLOW))
        options = ["firstname", "lastname"]
        lib_name = "fsearch"
        self.__display_options(lib_name, options)
        result = self.__get_multiple_options(lib_name, options)
        if not result: return
        firstname = result["firstname"]
        lastname = result["lastname"]
        temp_input = ""
        expected = ["y", "n"]
        fp.fprint(("Want to save the generated list ? (y/n)", fp.YELLOW))
        while temp_input not in expected:
            self.__set_prompt(lib_name, f'Enter {"/".join(expected)}')
            temp_input = input(self.prompt)
        possibilities = UsernameGenerator(firstname, lastname).possibilities
        fp.fprint(("[+] Generated " + str(len(possibilities)) + " usernames", fp.GREEN))

        if temp_input == "y":
            filename = firstname + "_" + lastname + "_" + str(datetime.timestamp(datetime.now()))
            self.__export_list_to_output(possibilities, filename, lambda x: x)

        found = []
       
        fp.fprint(("[+] Let's find ig accounts now ", fp.GREEN), ("O", fp.RED), ("_", fp.BLACK), ("O", fp.RED))
        for username in possibilities:
            try:
                response = self.__get_instagram_graph(username)
                if response.status_code == 200:
                    is_private = response.json()["graphql"]["user"]["is_private"]
                    if is_private:
                        fp.fprint(("[+]: ", fp.GREEN), (username, fp.YELLOW), (" PRIVATE", fp.RED))
                    else:
                        fp.fprint(("[+]: ", fp.GREEN), (username, fp.YELLOW), (" PUBLIC AYA", fp.GREEN))
                    found.append({
                        "username": username,
                        "is_private": is_private,
                        "url": f'https://www.instagram.com/{username}/',
                    })
            except Exception:
                pass

        filename = "result_" + firstname + "_" + lastname + "_" + str(datetime.timestamp(datetime.now()))
        self.__export_list_to_output(found, filename, lambda
            x: f'[{"PRIVATE" if x["is_private"] else "PUBLIC"}] {x["username"]}: {x["url"]}')
        fp.fprint(("\n[+] Found " + str(len(found)) + " accounts ", fp.GREEN), ("O", fp.RED), ("_", fp.BLACK),
                  ("O", fp.RED))
        self.__set_prompt()

    def help(self):
        for cmd_name in self.commands:
            fp.fprint(("[-] ", fp.GREEN), (cmd_name + ":", fp.YELLOW),
                      (self.commands[cmd_name]["description"], fp.GREEN))

    def __check_ig_session_id(self):
        if len(self.config["INSTAGRAM_SESSION_ID"]) == 0:
            fp.fprint(("Instagram session id is not set in config.json, edit and reload FINDER", fp.RED))
            return False
        return True

    def __get_instagram_graph(self,username):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': '*/*'
        }
        cookies = {
            'sessionid': self.config["INSTAGRAM_SESSION_ID"],
        }
        url = f'https://www.instagram.com/{username}/?__a=1&__d=dis'
        return requests.get(url, headers=headers, cookies=cookies, timeout=10)

    def __export_list_to_output(self, liste, __filename, func):
        filename = self.output_folder + "/" + __filename + ".txt"
        with open(filename, "w") as f:
            for item in liste:
                if item == liste[-1]:
                    f.write(func(item))
                else:
                    f.write(func(item) + "\n")
        fp.fprint(("Saved in " + os.path.abspath(filename), fp.GREEN))

    def __set_prompt(self, current_lib=None, text=""):
        if current_lib is None:
            self.prompt = f'[{self.name}] >>> '
        else:
            self.prompt = f'[{self.name}]-[{current_lib}] {text} >>> '

    def __clone_or_update(self, lib_name, url, folder):
        if (os.path.exists(folder)):
            subprocess.run(["git", "pull"], cwd=folder, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            fp.fprint((lib_name + " is already cloned so Finder updates it", fp.GREEN))
        else:
            subprocess.run(["git", "clone", url, folder], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def __pip_install(self, requirement_file):
        subprocess.run(["pip", "install", "-r", requirement_file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def __display_options(self, lib_name, options):
        fp.fprint(("Options for " + lib_name + " :", fp.YELLOW))
        fp.fprint((",".join(options) + "\n", fp.YELLOW))

    def __get_multiple_options(self, lib_name, options):
        result = {}
        for option in options:
            self.__set_prompt(lib_name, f'Enter {option}')
            temp_input = ""
            while len(temp_input) == 0:
                temp_input = input(self.prompt)
                if temp_input == "q":
                    fp.fprint((f"Cancel {lib_name}", fp.RED))
                    self.__set_prompt()
                    return None
                if len(temp_input) == 0:
                    fp.fprint(("Please provide a " + option + " value !", fp.RED))
            result[option] = temp_input
            self.__set_prompt(lib_name, "")
        return result

    def __install_by_pip(self, lib_name, github_url):
        fp.fprint((lib_name + " " + github_url, fp.MAGENTA))
        self.__clone_or_update(lib_name, github_url + ".git", self.vendor_folder + "/" + lib_name)
        fp.fprint(("Installing dependencies of " + lib_name + " ...", fp.MAGENTA))
        self.__pip_install(self.vendor_folder + "/" + lib_name + "/requirements.txt")
        fp.fprint((lib_name + " DONE", fp.GREEN))

    def test(self):
        return

    def _quit(self):
        fp.fprint(("We will find u anyway à_à", fp.RED))
        sys.exit(0)
