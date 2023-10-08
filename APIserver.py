from fastapi import FastAPI
from json import load
app = FastAPI()

@app.get("/items/{item}")
def read_item(item: str):
    if item == "mods":
        serverjson = ReadJsonFile("./datas/server.json")
        return serverjson["mods"]

# jsonファイルをpythonオブジェクトとして読み込みます 辞書型じゃね多分
def ReadJsonFile(path: str):
    with open(path, 'r') as file:
        return load(file)