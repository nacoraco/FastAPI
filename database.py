import sqlite3

# Create a SQLite database connection
conn = sqlite3.connect('FastAPI.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )
''')

# Insert sample data
cursor.execute('''
    INSERT INTO items (name, description) VALUES
    ('Item 1', 'Description of item 1'),
    ('Item 2', 'Description of item 2'),
    ('Item 3', 'Description of item 3')
''')

# Commit changes and close connection
conn.commit()
conn.close()
