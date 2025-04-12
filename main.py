from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

names = ['Jack', 'Jill', 'Alex', 'Sona']

@app.get('/')
def check():
    return {'message': 'All OK'}


@app.get('/names')
def get_names():
    return {'data': names}


@app.post('/names')
def insert_name(new_name):
    names.append(new_name)
    return {'data': names}


@app.put('/names/{id}')
def update_name(new_name, id):
    id = int(id)
    max_id = len(names)-1
    if id <= max_id:
        names[id] = new_name
        return {'data': names}
    else:
        raise Exception("Invalide ID")


@app.delete('/names/{id}')
def remove_name(id):
    id = int(id)
    max_id = len(names)-1
    if id <= max_id:
        del names[id]
        return {'data': names}
    else:
        raise Exception("Invalide ID")


