config_file = "config.json"

import json

def main():
    config = json.load(open(config_file))
    print("config: {}".format(config))

main()