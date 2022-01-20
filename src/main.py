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
        "hashed_password": "fakehashedvashistha",
        "disabled": False,
    },
    "anshuman": {
        "username": "anshuman",
        "full_name": "Anshuman Raj",
        "email": "anshuman@raj.com",
        "hashed_password": "fakehashedraj",
        "disabled": False,
    },
    "mayank": {
        "username": "mayank",
        "full_name": "Mayank Singh",
        "email": "mayank@singh.com",
        "hashed_password": "fakehashedsingh",
        "disabled": False,
    },
    "a": {
        "username": "a",
        "full_name": "ABC",
        "email": "abc@def.com",
        "hashed_password": "fakehasheda",
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

@app.get("/")
def init(s: str =Depends(get_current_active_user)):
    return {"Bug": "Tracking"}


@app.post("/bug/create/{bug_id}/{priority}/{type}/{posted_by}/{assigned_to}/{status}/{description}")
def create(bug_id: int, priority: int, type: str, posted_by: str, assigned_to: str, status: str, summary: str, description: str, s: str= Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    print("Connected to database")
    cur = conn.cursor()
    crr = conn.cursor()
    cuu = conn.cursor()
    today = datetime.datetime.now()
    dateTimeStr = str(today)
    cur.execute("INSERT INTO bugs(bug_id, priority, type, posted_by, assigned_to, status, summary, description, deadline, created_date, closed_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (bug_id, priority, type, posted_by, assigned_to, status, summary, description, 2*priority, dateTimeStr, dateTimeStr))
    cuu.execute("INSERT INTO logs(created_by, bug_id, event, created_date, closed_date) VALUES(%s, %s, %s, %s, %s);", (posted_by, bug_id, "created", dateTimeStr, dateTimeStr))
    crr.execute("SELECT name FROM users WHERE name = %s;", (posted_by))
    conn.commit()
    cuu.close()
    cur.close()
    conn.close()
    return {"Bug": "Created"}

@app.post("/bug/update/{bug_id}/{priority}/{type}/{posted_by}/{assigned_to}/{status}/{description}")
def update(bug_id: int, priority: int, type: str, posted_by: str, assigned_to: str, status: str, summary: str, description: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    print("Connected to database")
    cur = conn.cursor()
    crr = conn.cursor()
    cuu = conn.cursor()
    today = datetime.datetime.now()
    dateTimeStr = str(today)
    if status == "c":
        cur.execute("UPDATE bugs SET priority = %s, type = %s, posted_by = %s, assigned_to = %s, status = %s, summary = %s, description = %s, closed_date = %s WHERE bug_id = %s;", (priority, type, posted_by, assigned_to, status, summary, description, dateTimeStr, bug_id))
    cur.execute("UPDATE bugs SET priority = %s, type = %s, posted_by = %s, assigned_to = %s, status = %s, summary = %s, description = %s WHERE bug_id = %s;", (priority, type, posted_by, assigned_to, status, summary, description, bug_id))
    crr.execute("SELECT name FROM users WHERE name = %s;", (posted_by))
    cuu.execute("INSERT INTO logs(created_by, bug_id, event, created_date, closed_date) VALUES(%s, %s, %s, %s, %s);", (posted_by, bug_id, "created", dateTimeStr, dateTimeStr))
    conn.commit()
    crr.close()
    cuu.close()
    cur.close()
    conn.close()
    return {"Bug": "Updated"}

#@app.delete("/bug/delete/{bug_id}")
#def delete(bug_id: int, s: str=Depends(get_current_active_user)):
#    params = config()
#    conn = psycopg2.connect(**params)
#    cur = conn.cursor()
#    print("Connected to database")
#    cur.execute("DELETE FROM bugs WHERE bug_id = %s;", bug_id)
#    conn.commit()
#    cur.close()
#    conn.close()
#    return {"Bug ": "Deleted"}

@app.get("/bug/list/")
def list(s: str =Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    cur.execute("SELECT * FROM bugs;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
@app.get("/bug/assigned_to/{assigned_to}")
def list_by_assigned_to(assigned_to: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    cur.execute("SELECT * FROM bugs WHERE assigned_to=%s;", assigned_to)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/bug/status/{status}")
def list_by_status(status: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    cur.execute("SELECT * FROM bugs WHERE status=%s;", str(status))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/bug/posted_by/{posted_by}")
def list_by_posted_by(posted_by: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    crr = conn.cursor()
    print("Connected to database")
    cur.execute("SELECT * FROM bugs WHERE assigned_to=%s;", posted_by)
    crr.execute("SELECT name FROM users WHERE name = %s;", posted_by)
    rows = cur.fetchall()
    rows2 = crr.fetchall()
    crr.close()
    cur.close()
    conn.close()
    return rows+rows2

@app.get("/bug/priority/{priority}")
def list_by_priority(priority: str, s: str=Depends(get_current_active_user)):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    cur.execute("SELECT * FROM bugs WHERE priority=%s;", priority)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/bug/listlog/")
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