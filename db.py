import sqlite3


DB_NAME = 'tasks.db'

def init_db():
    connect = sqlite3.connect(DB_NAME)
    cursor = connect.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL      
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
                   )
""")
    
    connect.commit()
    connect.close()

def add_user_to_db(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        user_id = cursor.lastrowid
        return {"id" : user_id, "username" : username}
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_tasks_from_db(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, task, user_id FROM tasks WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    return [{"id" : r[0], "task" : r[1], "user_id" : r[2]} for r in rows]

def add_task_to_db(task, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (task, user_id) VALUES (?, ?)", (task, user_id))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {"id" : task_id, "task" : task, "user_id" : user_id}

def get_task_by_id(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, task, user_id FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id" : row[0], "task": row[1], "user_id" : row[2]}
    
    return None

def delete_task_by_id(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()

def update_task_in_db(task_id, new_task):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
    conn.commit()
    conn.close()