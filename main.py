from typing import Union
from fastapi import FastAPI
import sqlite3

app = FastAPI()

# Define a function to connect to the SQLite database
def get_db_conn():
    conn = sqlite3.connect('FastAPI.db')
    conn.row_factory = sqlite3.Row  # Enable accessing rows by column names
    return conn

# Endpoint to retrieve all items
@app.get("/items/")
def read_items():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return items

# Endpoint to retrieve a specific item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item
