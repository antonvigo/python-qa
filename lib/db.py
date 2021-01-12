import sqlite3

def connect_db():
    conn = sqlite3.connect("calcdb.db", check_same_thread=False)
    cursor = conn.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS results (
        id blob UNIQUE,
        operation text,
        result integer
    )
    """
    cursor.execute(sql)
    conn.commit()
    conn.row_factory = sqlite3.Row
    return conn
