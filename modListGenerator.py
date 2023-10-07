# mod list genarator ver 0.3
# by dynamiteOpanty

# よく分からなかったらfull setを実行すればOKです
# modpackに含まれるmod一つ一つのAPIをリクエストする処理で止まってしまった場合はctrl Cを連打して止めてください
# 再開する場合はメニューから"format mod list to readable"を選んでください

# TODO
# できたmodリストをhtml出力する
# exportされたmodpackのmanifest.jsonの解析
# まだmodpack.chからしか取得できないのでmodrinthにもAPIリクエストをできるようにする (面倒臭すぎるので放棄するかも 現に途中までやって放置してる)
# 比較モードの実装

from urllib import request as urlrequest
from json import load, loads, dumps
from os import path as ospath, mkdir, name as osname
import asyncio
try:
    from msvcrt import getch # type: ignore
except ImportError:
    from sys import stdin
    import termios # type: ignore
    def getch():
        # 標準入力のファイルディスクリプタ取得
        fd = stdin.fileno()
        # 属性を取得 old は戻す用
        old = termios.tcgetattr(fd) # type: ignore
        new = old.copy()
        # 設定を変更
        new[3] &= ~termios.ICANON # type: ignore
        new[3] &= ~termios.ECHO # type: ignore
        try:
            # 設定を反映
            termios.tcsetattr(fd, termios.TCSANOW, new) # type: ignore
            ch = stdin.read(1)
        finally:
            # 設定を元に戻す
            termios.tcsetattr(fd, termios.TCSANOW, old) # type: ignore
        # 文字表示
        return (ch)

baseDirectory = './'
modpackJson = f'{baseDirectory}modpack.json'
modlistJson = f'{baseDirectory}modlist.json'
readableJson = f'{baseDirectory}readable.json'
exportText = f'{baseDirectory}export.txt'

#メイン関数
def main():
    print("start process")
    while True:
        result = menu(["full set", "get raw mod pack", "get raw mod list", "format mod list to readable", "dependencies name fill", "export"], "select which mode to run. (q to exit)")
        if result == "cancel":
            exit()
        elif result == 0:
            GetModPack()
            GetModList()
            FormatModList_async()
            DependenciesNameFill()
            result = menu(["scrapbox text", "html"], "to what format?")
            if result == "cancel":
                continue
            elif result == 0:
                scrapbox()
            elif result == 1:
                print("WIP")
            exit()
        elif result == 1:
            GetModPack()
        elif result == 2:
            GetModList()
        elif result == 3:
            FormatModList_async()
            DependenciesNameFill()
        elif result == 4:
            DependenciesNameFill()
        elif result == 5:
            result = menu(["scrapbox text", "html"], "to what format?")
            if result == "cancel":
                continue
            elif result == 0:
                scrapbox()
            elif result == 1:
                print("WIP")
        print('finish')

# modpackの情報を取得します
def GetModPack():
    result = menu(["FTB", "curseforge", "modrinth"], "select which provider to target?")
    if result == 0:
        modpackID = input("input mod pack ID : ")
        print(f'fetching modpack ID={modpackID}')
        file = FTBAPIrequest(f'modpack/{modpackID}')
        file["provider"] = "modpackch"
        WriteJsonFile(modpackJson, file)
    elif result == 1:
        modpackID = input("input mod pack project ID :")
        print(f'fetching modpack ID={modpackID}')
        file = CurseforgeAPIRequest(modpackID)
        file["provider"] = "curseforge"
        WriteJsonFile(modpackJson, file)
    elif result == 2:
        modpackID = input("input mod pack project ID :")
        print(f'fetching modpack ID={modpackID}')
        file = ModrinthAPIRequest(f'project/{modpackID}')
        file["provider"] = "Modrinth"
        WriteJsonFile(modpackJson, file)

# modpackのmodリストを取得します
def GetModList():
    try:
        modpack = ReadJsonFile(modpackJson)
    except FileNotFoundError:
        print(get((f"{modpackJson}" " wasn't found. do 'get raw mod pack' process first."), Color.BG_RED))
        return
    modpackID = modpack["id"]
    modpackVersionList = []
    for i in modpack["versions"][-10:]:
        if modpack["provider"] == "Modrinth":
            version = ModrinthAPIRequest(f'version/{i}')
            modpackVersionList.append({"id" : version["id"], "name": version["name"]})
        else:
            modpackVersionList.append({"id": i["id"], "name": i["name"]})
    if modpack["provider"] == "Modrinth":
        modpackName = modpack["title"]
    else:
        modpackName = modpack["name"]
    result = menu([d['name'] for d in modpackVersionList], f'{modpackName}  select which version to process.')
    if result == "cancel":
        exit()
    else:
        modpackVersionID = modpackVersionList[result]["id"]
        if modpack["provider"] == "Modrinth":
            return WriteJsonFile(modlistJson, CleanModpack(ModrinthAPIRequest(f'version/{modpackVersionID}'))) #うまくいきません
        else:
            return WriteJsonFile(modlistJson, CleanModpack(FTBAPIrequest(f'modpack/{modpackID}/{modpackVersionID}')))

# modlistから必要な情報だけ抜き取って読みやすくします modrinth対応がまだです
def FormatModList_async():
    try:
        modlist = ReadJsonFile(modlistJson)
    except FileNotFoundError:
        print(get((f"{modlistJson}" " wasn't found. do 'get raw mod list' process first."), Color.BG_RED))
        return
    maxLength = len(modlist)
    startPoint = 0
    global Indent
    Indent = 0
    global doneCount
    doneCount = 0
    print(f'{maxLength} mods in total!')
    try:
        ReadJsonFile(readableJson)
        print(get(f'there is already {readableJson}!', Color.BG_GREEN))
        result = menu(['start over', 'resume'], f'start over or resume {readableJson}?')
        if result == 0:
            WriteJsonFile(readableJson, [])
        elif result == 1:
            startPoint = len(str(maxLength))
    except FileNotFoundError:
        WriteJsonFile(readableJson, [])
    try:
        remain = modlist[startPoint:]
        while not doneCount == maxLength:
            group = remain[:10]
            remain = remain[10:]
            tasks = [GenerateModdict_async(file, startPoint, maxLength) for file in group]
            loop = asyncio.get_event_loop()
            results = asyncio.gather(*tasks)
            result = loop.run_until_complete(results)
            WriteJsonFile(readableJson, ReadJsonFile(readableJson) + result)
    except KeyboardInterrupt:
        exit()

# fileリストから要らんものを掃除してmodだけにします
def CleanModpack(modpack):
    result = []
    for i in modpack["files"]:
        if i["type"] == "mod":
            result.append(i)
    return result

# modの要素を抜き出します
async def GenerateModdict_async(item, startPoint, maxLength):
    modDict = {}
    global Indent
    global doneCount
    try:
        loop = asyncio.get_event_loop()
        API = await loop.run_in_executor(None, FTBAPIrequest, f'mod/{item["curseforge"]["project"]}')
        modDict = {
            "id": API["id"],
            "name": API["name"],
            "description": API["description"],
            "art": API["art"][0]["url"],
            "link": API["links"][0]["link"],
            "latestVersion": API["versions"][0]["version"],
            "dependencies": DependenciesCheck(API["versions"][0], False)
        }
    except KeyError:
        modDict = {
            "id": item["id"],
            "error": "keyerror. assume this mod doesn't have curseforge id.",
            "name": item["name"],
            "directDownload": item["url"]
        }
    doneCount += 1
    if Indent < len(item["name"]):
        Indent = len(item["name"])
    space = "".rjust(Indent - len(item["name"]) + 1)
    doneCounter = get(f'({startPoint + doneCount}/{maxLength})'.rjust(3 + (len(str(maxLength)) * 2)), Color.CYAN)
    print(item["name"], f'{space}{doneCounter}')
    return modDict

# modの指定されたversionが依存している全てのプロジェクトのidを列挙します
# doNameFillがtrueだと毎回APIを呼んでnameも入れますが、そんなことしなくてもIDは取れてるので、一回mod全部の列挙が終わった後にリストからidを基準にmod名を読めばいいんじゃないかな
def DependenciesCheck(targetModVersion, doNameFill: bool = True):
    dependencies = []
    for mod in targetModVersion["dependencies"]:
        if doNameFill:
            API = FTBAPIrequest(f'/curseforge/{mod["id"]}')
            dependencies.append({"id": API["id"], "name": API["name"]})
        else:
            dependencies.append({"id": mod["id"], "name": None})
    return dependencies

# 上記の関数で空にしてたnameにmodの名前を入れていきます
def DependenciesNameFill():
    try:
        mods = ReadJsonFile(readableJson)
    except FileNotFoundError:
        print(get((f"{readableJson}" " wasn't found. do 'format mod list to readable' process first."), Color.BG_RED))
        return
    for i, mod in enumerate(mods):
        if not "error" in mod:
            for o, dependency in enumerate(mod["dependencies"]):
                dependMod = next(filter(lambda d: d.get(
                    "id") == dependency["id"], mods), None)
                if not dependMod == None:
                    pass
                    mods[i]["dependencies"][o]["name"] = dependMod["name"]
    WriteJsonFile(readableJson, mods)

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

# modpacks.ch/publicにAPIのリクエストを行います　headerとか要らんやろしbodyだけ持ってきてます
def FTBAPIrequest(target: str):
    return reqget(f'https://api.modpacks.ch/public/{target}')

# curseforgeにAPIのリクエストを行います　curseforge上のmodpackを取得するときのみ使用し、
# curseforge上のmodの取得にはFTBAPIrequest()を使用してください。
def CurseforgeAPIRequest(target: str):
    return FTBAPIrequest(f'curseforge/{target}')

def ModrinthAPIRequest(target: str):
    return reqget(f'https://api.modrinth.com/v2/{target}', header= { "User-Agent" :  "mod list generator py (a self study by a student. contact: )" })

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

# readableJsonをscrapbox向けテキストに変換します
def scrapbox(withLegend: bool = True):
    try:
        mods = ReadJsonFile(readableJson)
    except FileNotFoundError:
        print("readable.json wasn't found. do 'raw mod list' process first.")
        return
    resultText = ("mod list\n")
    if withLegend:
        resultText += ('''
[** [a mod name. with hyperlink to mod page http://google.com]]
 mods description.
  dependency mods here
  dependency mods here

''')
    for mod in mods:
        if "error" in mod:
            resultText += f'[** [{mod["name"].replace("[]", "").replace("]", "")} {mod["directDownload"]}]]\n'
            resultText += f'error: {mod["error"]}'
            resultText += '\n'
        else:
            resultText += f'[** [{mod["name"].replace("[", "").replace("]", "")} {mod["link"]}]]\n'
            # resulttext += 
            resultText += (f' {mod["description"]}\n')
            for dependency in mod["dependencies"]:
                resultText += (f'  {str(dependency["name"]).replace("[", "").replace("]", "")}\n')
            resultText += '\n'
    WriteTextFileScrapbox('./test.text', resultText)

# scrapbox向けのtextファイルを生成し書き込みます 返り値は書き込んだ内容
def WriteTextFileScrapbox(filepath: str, content: str):
    if not ospath.splitext(filepath)[1] == ".text":
        print("path doesn't end with '.text', please fix it later.")
        filepath = filepath + ".text"
    if not ospath.exists(ospath.dirname(filepath)):
        mkdir(ospath.dirname(filepath))
    with open(filepath, 'w') as file:
        file.write(content)
        return content

# こっから下はインターフェース
# 参考にしたサイト↓
# https://www.ytyng.com/blog/python-keyboard-menu-in-terminal-with-escape-sequence/

# キー入力を即座に受けます
def GetKeyInput():
    key = ord(getch())
    if key == Key.ENTER:
        return ('enter')
    elif key == Key.EOT:
        return KeyboardInterrupt
    elif key == Key.ESC:
        key = ord(getch())
        if key == ord('['):
            key = ord(getch())
        if key == Key.ARROWUP:
            return Key.ARROWUP
        elif key == Key.ARROWDOWN:
            return Key.ARROWDOWN
        elif key == Key.ARROWLEFT:
            return Key.ARROWLEFT
        elif key == Key.ARROWRIGHT:
            return Key.ARROWRIGHT
    else:
        return chr(key)

#キー入力のunicode値のうち重要なもので環境依存なものを正規化…正規化？します
class Key:
    ENTER = 13 if osname == "nt" else 10
    EOT = 3
    ESC = 224 if osname == "nt" else 27
    ARROWUP = 72 if osname  == "nt" else 65
    ARROWDOWN = 80 if osname == "nt" else 66
    ARROWLEFT = 75 if osname == "nt" else 68
    ARROWRIGHT = 77 if osname == "nt" else 67

# メニューを表示します
def menu(menuList: list, description: str = ''):
    current = 0
    c = ''
    while True:
        for i, item in enumerate(menuList):
            if current == i:
                print(get(f'> {item}', Color.BG_CYAN))
            else:
                print(get(f'  {item}', Color.MAGENTA))
        if description == '':
            print(get(f'c={repr(c)}, current={current}', Color.GREEN))
        else:
            print(get(description, Color.GREEN))
        c = GetKeyInput()
        if c == 'q':
            # q で終了
            return "cancel"
        elif c == 'enter':
            # エンターで決定
            print(f'selected:{get((menuList[current]), Color.YELLOW)}')
            return current
        if c == 'j' or c == Key.ARROWDOWN:
            # j か ↓　でカーソル移動
            if current < len(menuList) - 1:
                current += 1
        if c == 'k' or c == Key.ARROWUP:
            # k か ↑でカーソル移動
            if current > 0:
                current -= 1
        print(f'\033[{len(menuList) + 1}A', end='')

class Color:
    BLACK = '\033[30m'  # (文字)黒
    RED = '\033[31m'  # (文字)赤
    GREEN = '\033[32m'  # (文字)緑
    YELLOW = '\033[33m'  # (文字)黄
    BLUE = '\033[34m'  # (文字)青
    MAGENTA = '\033[35m'  # (文字)マゼンタ
    CYAN = '\033[36m'  # (文字)シアン
    WHITE = '\033[37m'  # (文字)白
    COLOR_DEFAULT = '\033[39m'  # 文字色をデフォルトに戻す
    BOLD = '\033[1m'  # 太字
    UNDERLINE = '\033[4m'  # 下線
    INVISIBLE = '\033[08m'  # 不可視
    REVERCE = '\033[07m'  # 文字色と背景色を反転
    BG_BLACK = '\033[40m'  # (背景)黒
    BG_RED = '\033[41m'  # (背景)赤
    BG_GREEN = '\033[42m'  # (背景)緑
    BG_YELLOW = '\033[43m'  # (背景)黄
    BG_BLUE = '\033[44m'  # (背景)青
    BG_MAGENTA = '\033[45m'  # (背景)マゼンタ
    BG_CYAN = '\033[46m'  # (背景)シアン
    BG_WHITE = '\033[47m'  # (背景)白
    BG_DEFAULT = '\033[49m'  # 背景色をデフォルトに戻す
    RESET = '\033[0m'  # 全てリセット

# テキストに色をつけて返します
def get(text: str, color = Color.COLOR_DEFAULT):
    return f'{color}{text}{Color.RESET}'

if __name__ == "__main__":
    main()
    # WriteJsonFile('./test.json', ModrinthAPIRequest('version/Ky04KgSQ'))