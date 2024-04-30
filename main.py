from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
from typing import List
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Define a function to connect to the SQLite database
def get_db_conn():
    conn = sqlite3.connect('FastAPI.db')
    conn.row_factory = sqlite3.Row  # Enable accessing rows by column names
    return conn

# Endpoint to retrieve all notes
@app.get("/notes/", response_class=HTMLResponse)
async def read_notes(request: Request):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes ORDER BY id DESC')
    notes = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

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
    

    # Endpoint to search notes by title
@app.get("/search/", response_class=HTMLResponse)
async def search_notes(request: Request, query: str):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE title LIKE ?", ('%' + query + '%',))
    notes = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

# Endpoint to create a new item

@app.post("/notes/", response_class=HTMLResponse)
async def create_item(request: Request, title: Optional[str] = None, text: Optional[List[str]] = None):
    # If title and text are not provided, create an empty note
    if title is None and text is None:
        title = "Naslov"
        text = ["Vsebina"]

    conn = get_db_conn()
    cursor = conn.cursor()
    for item_text in text:
        cursor.execute('INSERT INTO notes (title, text) VALUES (?, ?)', (title, item_text))
    conn.commit()
    
    # Fetch all notes after adding the new one
    cursor.execute('SELECT * FROM notes ORDER BY id DESC')
    notes = cursor.fetchall()
    
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})



# Endpoint to update an existing item
@app.put("/notes/{item_id}")
async def update_item(item_id: int, request: Request):
  # Parse request body as JSON
  data = await request.json()
  title = data.get("title")
  text = data.get("text")

  # Check if ID exists
  conn = get_db_conn()
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM notes WHERE id = ?', (item_id,))
  existing_item = cursor.fetchone()
  conn.close()
  if existing_item is None:
      raise HTTPException(status_code=404, detail="Item not found")

  # Update database
  conn = get_db_conn()
  cursor = conn.cursor()
  cursor.execute('UPDATE notes SET title = ?, text = ? WHERE id = ?', (title, text, item_id))
  conn.commit()
  conn.close()

  return {"message": "Note updated successfully"}

# Endpoint to delete a specific item by ID

@app.delete("/delnotes/{item_id}")
def delete_item(item_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()

    # Check if ID exists
    cursor.execute('SELECT * FROM notes WHERE id = ?', (item_id,))
    existing_item = cursor.fetchone()
    if existing_item is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")

    cursor.execute('DELETE FROM notes WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

    return {"message": "Item deleted successfully"}
