#version 0.0

import menu
import urllib
import json
import dynaModules
from os import path as ospath, mkdir
import shutil
import asyncio

def main():
    configpath = "./config.json"
    config = dynaModules.ReadJsonFile(configpath)
    instancePath = config["instancePath"]
    if not ospath.exists("./datas"):
        mkdir("./datas")
    dynaModules.WriteJsonFile("./datas/test3.json", MainServerAPIRequest("mods"))
    # dynaModules.WriteJsonFile("./datas/test1.json", ModrinthAPIRequest("project/Xbc0uyRg"))
    # dynaModules.WriteJsonFile("./datas/test2.json", ModrinthAPIRequest("project/Xbc0uyRg/version"))
    mods = dynaModules.ReadJsonFile("./datas/test3.json")
    content = [f'{i["title"]}' for i in mods["mods"]]
    menu.scroll(screen_lines=min(len(content) + 2, shutil.get_terminal_size().lines), content= content)


def ModrinthAPIRequest(target: str):
    return dynaModules.reqget(f'https://api.modrinth.com/v2/{target}', header= {"User-Agent" : "mod updater py \n self study by a student contact: matunyan0930@gmail.com"})

def MainServerAPIRequest(target: str):
    try:
        return dynaModules.reqget(f"http://127.0.0.1:8000/items/{target}")
    except dynaModules.reqgeterror:
        print("couldn't reach the server. make sure the IP is correct, or expect server is down now.")
        return {"detail": "error, couldn't reach the server"}

if __name__=="__main__":
    main()