from fastmcp import FastMCP
import aiosqlite
import os
import tempfile

# Works on Windows, Mac, Linux, and Docker cloud
DB_PATH = os.path.join(tempfile.gettempdir(), "expenses.db")

mcp = FastMCP("expense-tracker")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
        await conn.commit()

@mcp.tool()
async def add_expense(date, amount, category, subcategory="", note=""):
    async with aiosqlite.connect(DB_PATH) as conn:
        cur = await conn.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        await conn.commit()
        return {'status': "ok", "id": cur.lastrowid}

@mcp.tool()
async def list_expenses():
    async with aiosqlite.connect(DB_PATH) as conn:
        cur = await conn.execute(
            "SELECT id, date, amount, category, subcategory, note FROM expenses ORDER BY id ASC"
        )
        cols = [d[0] for d in cur.description]
        rows = await cur.fetchall()
        return [dict(zip(cols, r)) for r in rows]

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())  # Initialize DB before starting server
    mcp.run(transport="http", host="0.0.0.0", port=8000)

# to run == uv run main.py
# to inspect == uv run fastmcp dev inspector main.py