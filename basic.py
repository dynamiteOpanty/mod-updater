from urllib import request as urlrequest, error as urlliberror
from json import load, loads, dumps
from os import path as ospath, mkdir

class reqgeterror(Exception):
    pass
# APIリクエストの本体です
def reqget(URL: str, debug: bool = False, header = None):
    if not header == None:
        get_req = urlrequest.Request(URL, headers=header)
    else:
        get_req = urlrequest.Request(URL)
    try:
        with urlrequest.urlopen(get_req) as res:
            body = loads(res.read())
            if debug:
                print(body)
            return body
    except urlliberror.URLError:
        raise reqgeterror
    except KeyboardInterrupt:
        exit()

# jsonファイルを生成し書き込みます 返り値は書き込んだ内容　よくテストしてないんだけど多分引数は辞書型でも辞書型みたいな面した文字型でもok
def WriteJsonFile(filepath: str, content: list | dict):
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