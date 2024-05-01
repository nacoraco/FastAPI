from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from passlib.context import CryptContext
from database import initialize_database
from fastapi import Form
from typing import List
import sqlite3

initialize_database()

app = FastAPI()

# Za hashiranje gesel
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory="templates")


# Define a function to connect to the SQLite database
def get_db_conn():
    conn = sqlite3.connect('FastAPI.db')
    conn.row_factory = sqlite3.Row  # Enable accessing rows by column names
    return conn


# Model za prijavo
class UserLogin(BaseModel):
    username: str
    password: str

# Model za registracijo
class UserRegister(BaseModel):
    username: str
    password: str


# Metoda za preverjanje gesla
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Metoda za hashiranje gesla
def hash_password(password):
    return pwd_context.hash(password)


# API endpoint za prijavo
@app.post("/login/")
async def login(user: UserLogin):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password_hash FROM users WHERE username=?", (user.username,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        username, password_hash = user_data
        if verify_password(user.password, password_hash):
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# API endpoint za registracijo
@app.post("/register/")
async def register(user: UserRegister):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (user.username,))
    existing_user = cursor.fetchone()
    conn.close()
    if existing_user:
        raise HTTPException(status_code=400, detail="Uporabniško ime že obstaja")

    # Hashiraj geslo
    hashed_password = hash_password(user.password)

    # Shrani uporabnika v bazo
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (user.username, hashed_password))
    conn.commit()
    conn.close()

    return {"message": "Uporabnik uspešno registriran"}


# Endpoint to retrieve all notes
@app.get("/notes/", response_class=HTMLResponse)
async def read_notes(request: Request):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes ORDER BY id DESC')
    notes = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})


# Endpoint to retrieve a specific user
@app.get("/notes/{user_id}")
def read_item(user_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE user_id = ?', (user_id,))
    item = cursor.fetchall()
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
