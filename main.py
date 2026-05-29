from fastmcp import FastMCP
import os 
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP("expense-tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as C:
        C.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                 amount REAL NOT NULL,
                 category TEXT NOT NULL,
                 subcategory TEXT DEFAULT '',
                 note TEXT DEFAULT ''
            )
        """)
init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    with sqlite3.connect(DB_PATH) as C:
        cur = C.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
            )
        
        return {'status': "ok", "id":cur.lastrowid }

@mcp.tool()
def list_expenses():
    with sqlite3.connect(DB_PATH) as C:
        cur = C.execute("SELECT id, date, amount, category, subcategory, note FROM expenses ORDER BY id ASC")
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

# Start Server


if __name__ == "__main__":
    mcp.run(transport="http", host= "0.0.0.0", port=8000) #major change

# to run == uv run main.py
# to inspect == uv run fastmcp dev inspector main.py