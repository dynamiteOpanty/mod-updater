#version 0.0

import menu
import dynaModules
from urllib import request as urlrequest
from json import load, loads, dumps
from os import path as ospath, mkdir
import asyncio

def main():
    configpath = "./config.json"
    config = dynaModules.ReadJsonFile(configpath)
    instancePath = config["instancePath"]
    if not ospath.exists("./datas"):
        mkdir("./datas")
    dynaModules.WriteJsonFile("./datas/test1.json", ModrinthAPIRequest("project/P7dR8mSH"))
    dynaModules.WriteJsonFile("./datas/test2.json", ModrinthAPIRequest("project/P7dR8mSH/version"))

def ModrinthAPIRequest(target: str):
    return dynaModules.reqget(f'https://api.modrinth.com/v2/{target}', header= {"User-Agent" : "mod updater py \n self study by a student contact: matunyan0930@gmail.com"})

if __name__=="__main__":
    main()