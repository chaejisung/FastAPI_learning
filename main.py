from enum import Enum
from fastapi import FastAPI

class itemID(int, Enum):
    id1 = '111'
    id2 = '222'

app = FastAPI()

@app.get('/items/{items_id}')
async def root(items_id: itemID):
    return {'message': items_id}

