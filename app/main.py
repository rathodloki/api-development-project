from telnetlib import STATUS
from typing import Optional
from unittest import result
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2, time
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(dbname='fastapi',user='postgres',password='1234',cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Database connection successfull")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:",error)
        time.sleep(2)

app = FastAPI()
class Users(BaseModel):
    name: str
    occupation: Optional[str] = ""
    age: int

# temp requests
@app.get("/test_db")
def test_db():
    cur.execute("SELECT * FROM users;")
    records = cur.fetchall()
    return records

@app.get("/")
def read_root():
    return {"Hello": "World"}

#get all users
@app.get("/users")
def get_users():
    cur.execute("SELECT * FROM users;")
    records = cur.fetchall()
    return records

#create user request
@app.post("/users",status_code=status.HTTP_201_CREATED)
def add_user(data: Users):
    cur.execute("INSERT INTO users (name, occupation, age) VALUES ('{0}', '{1}', '{2}') RETURNING *;".format(str(data.name),str(data.occupation),data.age))
    result=cur.fetchone()
    conn.commit()
    return result

#get specific user
@app.get("/users/{id}")
def get_user(id: int, response: Response):
    cur.execute("SELECT * FROM users where id=%s;"%str(id))
    user=cur.fetchone()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user    

#delete user
@app.delete("/users/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_user(id: int, response: Response):
    if(id == 0):
        cur.execute("DELETE FROM users returning *;")
    else:
        cur.execute("DELETE FROM users where id=%s returning *;"%str(id))
    result=cur.fetchone()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update user
@app.put("/users/{id}",status_code=status.HTTP_201_CREATED)
def update_user(id:int,users: Users, response: Response):
    cur.execute("UPDATE users SET name='{}', occupation='{}', age='{}' where id = '{}' RETURNING *;".format(str(users.name),str(users.occupation),str(users.age), str(id)))
    result = cur.fetchone()
    conn.commit()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return result