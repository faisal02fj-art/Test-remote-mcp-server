from fastmcp import FastMCP
import sqlite3
import os
import tempfile

# Works on Windows, Mac, Linux, and Docker cloud
DB_PATH = os.path.join(tempfile.gettempdir(), "expenses.db")

mcp = FastMCP("expense-tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
        conn.commit()

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        conn.commit()
        return {'status': "ok", "id": cur.lastrowid}

@mcp.tool()
def list_expenses():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT id, date, amount, category, subcategory, note FROM expenses ORDER BY id ASC")
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
# to run == uv run main.py
# to inspect == uv run fastmcp dev inspector main.py