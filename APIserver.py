from fastapi import FastAPI
import basic

app = FastAPI()

@app.get("/items/{item}")
def read_item(item: str):
    if item == "mods":
        serverjson = basic.ReadJsonFile("./server/mods.json")
        return serverjson