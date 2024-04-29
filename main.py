from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from database import initialize_database
import sqlite3

initialize_database()

app = FastAPI()

# Define a function to connect to the SQLite database
def get_db_conn():
    conn = sqlite3.connect('FastAPI.db')
    conn.row_factory = sqlite3.Row  # Enable accessing rows by column names
    return conn

# Endpoint to retrieve all notes
@app.get("/notes/")
def read_notes():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    conn.close()
    return notes

# Endpoint to retrieve a specific item by ID
@app.get("/notes/{item_id}")
def read_item(item_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Endpoint to create a new item
@app.post("/notes/")
def create_item(title: str, text: Optional[str] = None):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (title, text) VALUES (?, ?)', (title, text))
    conn.commit()
    new_item_id = cursor.lastrowid
    conn.close()
    return {"id": new_item_id, "title": title, "text": text}


# Endpoint to update an existing item
@app.put("/notes/{item_id}")
def update_item(item_id: int, title: str, text: Optional[str] = None):
    conn = get_db_conn()
    cursor = conn.cursor()

    # Preveri, ali obstaja zapis z določenim ID-jem
    cursor.execute('SELECT * FROM notes WHERE id = ?', (item_id,))
    existing_item = cursor.fetchone()
    if existing_item is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")

    cursor.execute('UPDATE notes SET title = ?, text = ? WHERE id = ?', (title, text, item_id))
    conn.commit()
    conn.close()

    return {"id": item_id, "title": title, "text": text}


# Endpoint to delete an existing item
@app.delete("/notes/{item_id}")
def delete_item(item_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()

    # Preveri, ali obstaja zapis z določenim ID-jem
    cursor.execute('SELECT * FROM notes WHERE id = ?', (item_id,))
    existing_item = cursor.fetchone()
    if existing_item is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")

    cursor.execute('DELETE FROM notes WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

    return {"message": "Item deleted successfully"}
