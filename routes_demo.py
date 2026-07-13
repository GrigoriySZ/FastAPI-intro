from fastapi import FastAPI

app = FastAPI(
    title = 'Демо маршрутизации',
    description = 'Пример HTTP методов',
    verson='1.0.0'
)

async def patch_item(item_id: id, name: str=None): 
    return {"id": item_id, "name": name, "patched": True}

@app.get('/items', summary="Получить список всех элементов")
async def get_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

@app.get('/item/{item_id}')
async def get_item(item_id: int): 
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.post('/items')
async def create_item(name: str):
    return {"id": 3, "name": name}

@app.put('/items/{item_id}')
async def update_item(item_id: int, name: str):
    return {"id": item_id, "name": name, "updatued": True}

@app.delete('/items/{item_id}')
async def delete_item(item_id: int):
    return {"id": item_id, "deleted": True}

@app.patch('/items/{item_id}')
async def patch_item(item_id: int, name: str=None):
    return {"id": item_id, "name": name, "patched": True}