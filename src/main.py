#!/usr/bin/python

import psycopg2

from config import config
import datetime

from fastapi import FastAPI

from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
users = {
    "shikhar": {
        "username": "shikhar",
        "full_name": "Shikhar Vashistha",
        "email": "shikhar@vashistha.com",
        "hashed_password": "fakehashed123",
        "disabled": False,
    },
}

app = FastAPI()

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(users, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

#@app.get("/")
#def init(s: str =Depends(get_current_active_user)):
#    return {"Order": "Tracking"}


@app.post("/order/create/{order_id}/{priority}/{type}/{posted_by}/{assigned_to}/{status}/{description}")
def create(order_id: str, priority: int, type: str, posted_by: str, assigned_to: str, status: str, summary: str, description: str, s: str= Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    print("Connected to database")
    cur = conn.cursor()
    cuu = conn.cursor()
    today = datetime.datetime.now()
    dateTimeStr = str(today)
    cur.execute("INSERT INTO orders(order_id, priority, type, posted_by, assigned_to, status, summary, description, deadline, created_date, closed_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (order_id, priority, type, posted_by, assigned_to, status, summary, description, 2*priority, dateTimeStr, dateTimeStr))
    cuu.execute("INSERT INTO logs(created_by, order_id, event, created_date, closed_date) VALUES(%s, %s, %s, %s, %s);", (s.username, order_id, "created", dateTimeStr, dateTimeStr))
    conn.commit()
    cuu.close()
    cur.close()
    conn.close()
    return {"Order": "Created"}

@app.post("/order/update/{order_id}/{priority}/{type}/{posted_by}/{assigned_to}/{status}/{description}")
def update(order_id: str, priority: int, type: str, posted_by: str, assigned_to: str, status: str, summary: str, description: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    print("Connected to database")
    cur = conn.cursor()
    cuu = conn.cursor()
    today = datetime.datetime.now()
    dateTimeStr = str(today)
    if status == "c":
        cur.execute("UPDATE orders SET priority = %s, type = %s, posted_by = %s, assigned_to = %s, status = %s, summary = %s, description = %s, closed_date = %s WHERE order_id = %s;", (priority, type, posted_by, assigned_to, status, summary, description, dateTimeStr, order_id))
    cur.execute("UPDATE orders SET priority = %s, type = %s, posted_by = %s, assigned_to = %s, status = %s, summary = %s, description = %s WHERE order_id = %s;", (priority, type, posted_by, assigned_to, status, summary, description, order_id))
    cuu.execute("INSERT INTO logs(created_by, order_id, event, created_date, closed_date) VALUES(%s, %s, %s, %s, %s);", (s.username, order_id, "updated", dateTimeStr, dateTimeStr))
    conn.commit()
    cuu.close()
    cur.close()
    conn.close()
    return {"Order": "Updated"}

@app.delete("/order/delete/{order_id}")
def delete(order_id: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cuu = conn.cursor()
    print("Connected to database")
    order_id = str(order_id)
    cur.execute("DELETE FROM orders WHERE order_id = %s;", (order_id,))
    cuu.execute("INSERT INTO logs(created_by, order_id, event, created_date, closed_date) VALUES(%s, %s, %s, %s, %s);", (s.username, order_id, "deleted", datetime.datetime.now(), datetime.datetime.now()))
    conn.commit()
    cuu.close()
    cur.close()
    conn.close()
    return {"Order ": "Deleted"}

@app.get("/order/list/")
def list(s: str =Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    cur.execute("SELECT * FROM orders;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
@app.get("/order/assigned_to/{assigned_to}")
def list_by_assigned_to(assigned_to: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    assigned_to = str(assigned_to)
    cur.execute("SELECT * FROM orders WHERE assigned_to = %s;", (assigned_to,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/order/{status}")
def list_by_status(status: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    status = str(status)
    cur.execute("SELECT * FROM orders WHERE status = %s;", (status,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/order/posted_by/{posted_by}")
def list_by_posted_by(posted_by: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    posted_by = str(posted_by)
    cur.execute("SELECT * FROM orders WHERE posted_by = %s;", (posted_by,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/order/priority/{priority}")
def list_by_priority(priority: int, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    priority = int(priority)
    cur.execute("SELECT * FROM orders WHERE priority = %s;", (priority,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/order/listlog/")
def listlog(s: str =Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    cur.execute("SELECT * FROM logs;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
def main():
    pass


if __name__ == '__main__':
	main()