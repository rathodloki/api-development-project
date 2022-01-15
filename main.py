from telnetlib import STATUS
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()
tempdb=[{"id": 1, "name": "lokendar", "occupation": "Engineer", "age": 22},{"id": 2, "name": "loki", "occupation": "dev", "age": 23}]
class Users(BaseModel):
    name: str
    occupation: str
    age: float

def find_user(id):
    for user in tempdb:
        if id == user["id"]:
            return user

def find_user_index(id):
    for index, user in enumerate(tempdb):
        if user["id"] == id:
            return index

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def get_users():
    return tempdb

@app.post("/users",status_code=status.HTTP_201_CREATED)
def add_user(data: Users):
    id=len(tempdb)
    tempdb.append({"id":id+1, "name": data.name, "occupation": data.occupation, "age": data.age})
    return {"id":id+1, "name": data.name, "occupation": data.occupation, "age": data.age}

@app.get("/users/{id}")
def get_user(id: int, response: Response):
    user=find_user(id)
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user    

@app.delete("/users/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_user(id: int, response: Response):
    index=find_user_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    tempdb.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/users/{id}",status_code=status.HTTP_201_CREATED)
def update_user(id:int,users: Users, response: Response):
    index=find_user_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    user=users.dict()
    user["id"]=id
    tempdb[index]=user
    return tempdb[index]