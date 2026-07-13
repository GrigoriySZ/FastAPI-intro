from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# uvicorn exceprion_demo:app --reload --host 127.0.0.1 --port 8000

app = FastAPI()

data_db = {
    1: {"name": "Test 1"},
    2: {"name": "Test 2"},
    3: {"name": "Test 3"},
}

@app.get('/data/{id}')
async def get_data(id: int):
    if id not in data_db:
        raise HTTPException(
            status_code=404,
            detail=f'Data with id {id} not found'
        )
    return data_db[id]

@app.get('/data')
async def get_data():
    return {"key": "value"}

@app.post('/data', status_code=201)
async def crate_data(): 
    return {"id": 1, "name": "New item"}

@app.get('/custom')
async def custom_response():
    return JSONResponse(
        content={'message': 'Custom response'},
        status_code=200,
        headers={'X-Custom-Header': 'value'}
    )