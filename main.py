from typing import Union, Optional
from fastapi import FastAPI, HTTPException
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
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Endpoint to create a new item
@app.post("/items/")
def create_item(name: str, description: Optional[str] = None):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    new_item_id = cursor.lastrowid
    conn.close()
    return {"id": new_item_id, "name": name, "description": description}

# Endpoint to update an existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, description: Optional[str] = None):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (name, description, item_id))
    conn.commit()
    conn.close()
    return {"id": item_id, "name": name, "description": description}

# Endpoint to delete an existing item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully"}
