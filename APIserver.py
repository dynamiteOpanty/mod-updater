from fastapi import FastAPI
import dynaModules

app = FastAPI()

@app.get("/items/{item}")
def read_item(item: str):
    if item == "mods":
        serverjson = dynaModules.ReadJsonFile("./server/mods.json")
        return serverjson