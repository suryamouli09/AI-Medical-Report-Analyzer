import sqlite3
import bcrypt

# ─────────────────────────────────────────────
# Database Connection
# ─────────────────────────────────────────────

DB_NAME = "users.db"

# ─────────────────────────────────────────────
# Initialize Database
# ─────────────────────────────────────────────

def init_db():

    conn = sqlite3.connect(DB_NAME)

    c = conn.cursor()

    c.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT
        )

    """)

    conn.commit()

    conn.close()

# ─────────────────────────────────────────────
# Create User
# ─────────────────────────────────────────────

def create_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    c = conn.cursor()

    # Hash password
    hashed = bcrypt.hashpw(

        password.encode(),

        bcrypt.gensalt()
    )

    try:

        c.execute(

            "INSERT INTO users (username, password) VALUES (?, ?)",

            (username, hashed)
        )

        conn.commit()

        conn.close()

        return True

    except:

        conn.close()

        return False

# ─────────────────────────────────────────────
# Login Validation
# ─────────────────────────────────────────────

def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    c = conn.cursor()

    c.execute(

        "SELECT password FROM users WHERE username=?",

        (username,)
    )

    data = c.fetchone()

    conn.close()

    if data is None:

        return False

    stored_password = data[0]

    return bcrypt.checkpw(

        password.encode(),

        stored_password
    )