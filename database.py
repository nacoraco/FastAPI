import sqlite3

def initialize_database():
    # Create a SQLite database connection
    conn = sqlite3.connect('FastAPI.db')
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            text TEXT
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

# If the script is run directly, initialize the database
if __name__ == "__main__":
    initialize_database()
