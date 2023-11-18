import sqlite3 as sql


async def sql_connector():
    con = sql.connect("youtube.db")
    cur = con.cursor()
    return con, cur


async def create_tables():
    con, cur = await sql_connector()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY
        )""")

async def add_user(user_id: int):
    con, cur = await sql_connector()
    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()

    if not user:
        cur.execute("INSERT INTO users VALUES (?)", (user_id,))
        con.commit()


async def get_all_users():
    con, cur = await sql_connector()
    
    users = cur.execute("SELECT * FROM users").fetchone()
    return len(users)


async def get_all_id():
    con, cur = await sql_connector()
    
    users = cur.execute("SELECT user_id FROM users").fetchall()
    return users
