#version 0.0

import menu
from urllib import request as urlrequest
from json import load, loads, dumps
from os import path as ospath, mkdir
import asyncio

def main():
    configpath = "./config.json"
    config = ReadJsonFile(configpath)
    instancePath = config["instancePath"]
    if not ospath.exists("./datas"):
        mkdir("./datas")
    WriteJsonFile("./datas/test1.json", reqget("https://api.modrinth.com/v2/project/P7dR8mSH"))
    WriteJsonFile("./datas/test2.json", reqget("https://api.modrinth.com/v2/project/P7dR8mSH/version"))

def ModrinthAPIRequest(target: str):
    return reqget(f'https://api.modrinth.com/v2/{target}', header= {"User-Agent" : "mod updater py \n self study by a student contact: matunyan0930@gmail.com"})

# APIリクエストの本体です
def reqget(URL: str, debug: bool = False, header = None):
    if not header == None:
        get_req = urlrequest.Request(URL, headers=header)
    else:
        get_req = urlrequest.Request(URL)
    with urlrequest.urlopen(get_req) as res:
        body = loads(res.read())
        if debug:
            print(body)
        return body

# jsonファイルを生成し書き込みます 返り値は書き込んだ内容　よくテストしてないんだけど多分引数は辞書型でも辞書型みたいな面した文字型でもok
def WriteJsonFile(filepath: str, content: list):
    if not ospath.splitext(filepath)[1] == ".json":
        print("path doesn't end with '.json', please fix it later.")
        filepath = filepath + ".json"
    if not ospath.exists(ospath.dirname(filepath)):
        mkdir(ospath.dirname(filepath))
    with open(filepath, 'w') as file:
        file.write(dumps(content, indent=4))
        return content

# jsonファイルをpythonオブジェクトとして読み込みます 辞書型じゃね多分
def ReadJsonFile(path: str):
    with open(path, 'r') as file:
        return load(file)

if __name__=="__main__":
    main()