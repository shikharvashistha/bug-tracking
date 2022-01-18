#!/usr/bin/python

import psycopg2

from config import config

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def init():
    return {"Bug": "Tracking"}


@app.get("/bug/create/{bug_id}/{priority}/{type}/{posted_by}/{assigned_to}/{status}/{description}")
def create(bug_id: int, priority: int, type: str, posted_by: str, assigned_to: str, status: str, summary: str, description: str):
    params = config()
    conn = psycopg2.connect(**params)
    print("Connected to database")
    cur = conn.cursor()
    cur.execute("INSERT INTO bugs (bug_id, priority, type, posted_by, assigned_to, status, summary, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (bug_id, priority, type, posted_by, assigned_to, status, summary, description))
    conn.commit()
    cur.close()
    conn.close()
    return {"Bug": "Created"}

@app.post("/bug/update/{bug_id}/{priority}/{type}/{posted_by}/{assigned_to}/{status}/{description}")
def update(bug_id: int, priority: int, type: str, posted_by: str, assigned_to: str, status: str, summary: str, description: str):
    params = config()
    conn = psycopg2.connect(**params)
    print("Connected to database")
    cur = conn.cursor()
    cur.execute("UPDATE bugs SET priority = %s, type = %s, posted_by = %s, assigned_to = %s, status = %s, summary = %s, description = %s WHERE bug_id = %s;", (priority, type, posted_by, assigned_to, status, summary, description, bug_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"Bug": "Updated"}

@app.delete("/bug/delete/{bug_id}")
def delete(bug_id: int):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    cur.execute("DELETE FROM bugs WHERE bug_id = %s;", (bug_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"Bug ": "Deleted"}

@app.get("/bug/list/")
def list():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print("Connected to database")
    cur.execute("SELECT * FROM bugs;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def main():
    pass


if __name__ == '__main__':
	main()