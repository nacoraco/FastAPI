import sqlite3


def initialize_database():
    # Create a SQLite database connection
    conn = sqlite3.connect('FastAPI.db')
    cursor = conn.cursor()

    # Create a table for notes
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                text TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


# If the script is run directly, initialize the database
if __name__ == "__main__":
    initialize_database()
