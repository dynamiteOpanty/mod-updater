#version 0.0

import menu
import dynaModules
from os import path as ospath, mkdir
import shutil
import asyncio

configpath = "./config.json"
datasDir = "./datas/"
modsDir = f'{datasDir}mods/'
config = dynaModules.ReadJsonFile(configpath)

def main():
    instancePath = config["instancePath"]
    if not ospath.exists(datasDir):
        mkdir(datasDir)
    if not ospath.exists(modsDir):
        mkdir(modsDir)
    dynaModules.WriteJsonFile(f'{datasDir}serverStatus.json', MainServerAPIRequest("mods"))
    mods = dynaModules.ReadJsonFile(f'{datasDir}serverStatus.json')
    for item in mods["mods"]:
        dir = f'{modsDir}{item["id"]}'
        if not ospath.exists(dir):
            mkdir(dir)
    tasks = [ModrinthEachModRequest(item["id"]) for item in mods["mods"]]
    loop = asyncio.get_event_loop()
    gather = asyncio.gather(*tasks)
    loop.run_until_complete(gather)

    # content = [f'{i["title"]}' for i in mods["mods"]]
    # menu.scroll(screen_lines=min(len(content) + 2, shutil.get_terminal_size().lines), content= content)

async def ModrinthEachModRequest(projectID: str):
    loop = asyncio.get_event_loop()
    dynaModules.WriteJsonFile(f'{modsDir}{projectID}/project.json', await  loop.run_in_executor(None, ModrinthAPIRequest, f'project/{projectID}'))
    dynaModules.WriteJsonFile(f'{modsDir}{projectID}/versions.json', await loop.run_in_executor(None, ModrinthAPIRequest, f'project/{projectID}/version'))

def ModrinthAPIRequest(target: str):
    return dynaModules.reqget(f'https://api.modrinth.com/v2/{target}', header= {"User-Agent" : "mod updater py \n self study by a student contact: matunyan0930@gmail.com"})

def MainServerAPIRequest(target: str):
    try:
        return dynaModules.reqget(f"http://{config['serverip']}:8000/items/{target}")
    except dynaModules.reqgeterror:
        print("couldn't reach the server. make sure the IP is correct, or expect server is down now.")
        exit()

if __name__=="__main__":
    main()