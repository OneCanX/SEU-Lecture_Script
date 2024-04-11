import json

config = json.load(open('config.json', 'r', encoding='utf-8'))
# login #
username = config["login"]["username"]
password = config["login"]["password"]

# main #
interval = config["thread"]["interval"]
thread_num = config["thread"]["thread_num"]
vcode_interval = 10
