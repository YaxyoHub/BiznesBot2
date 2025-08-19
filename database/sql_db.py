import sqlite3

DB_NAME = "business.db"

class init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "name TEXT NOT NULL,"
    "username TEXT,"
    "phone_number TEXT,"
    "telegram_id INTEGER UNIQUE);"
    )

    cursor.execute("CREATE TABLE IF NOT EXISTS admins ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "name TEXT NOT NULL,"
    "username TEXT UNIQUE,"
    "phone TEXT,"
    "telegram_id INTEGER UNIQUE"
    ");"
    )
    conn.commit()
    cursor.close()
    conn.close()

""" User """
# def alter():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("ALTER TABLE users ADD COLUMN business TEXT;")
#     conn.commit()
#     cursor.close()
#     conn.close()

# alter()
# print("boldi")

def get_user_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM users;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_user_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def add_user(telegram_id, name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
        conn.commit()
    conn.close()


def update_user_info(telegram_id, name, username, phone, business):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET name = ?, username = ?, phone_number = ?, business = ?
        WHERE telegram_id = ?
    """, (name, username, phone, business, telegram_id))
    conn.commit()
    conn.close()

""" User """
"""+=====================================================================+"""
""" Admin """

def add_admin(name, username, phone, telegram_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admins (name, username, phone, telegram_id)" 
    "VALUES (?, ?, ?, ?);", (name, username, phone, telegram_id,))
    conn.commit()
    cursor.close()
    conn.close()

# add_admin(
#     'Yaxyo', '@Yaxyo2008', '+9989421405510', 6150566915
# )

# print("Admin qo'shildi")

def delete_admin(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admins WHERE telegram_id = ?;", (id,))
    conn.commit()
    cursor.close()
    conn.close()

def check_admin(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE telegram_id = ?;", (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

def get_admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data 

""" Admin """