from fastmcp import FastMCP
import os 
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP("expense-tracker")

def init_db():
    """Initialize database with proper error handling and permissions"""
    try:
        # Ensure the database directory exists and is writable
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, mode=0o755)
        
        # Create/connect to database with explicit write mode
        with sqlite3.connect(DB_PATH, timeout=10) as conn:
            # Disable journal to avoid locking issues
            conn.isolation_level = None  # autocommit mode
            
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
        
        # Ensure file has proper permissions (readable/writable by all)
        if os.path.exists(DB_PATH):
            os.chmod(DB_PATH, 0o666)
        
        print(f"✓ Database initialized at {DB_PATH}")
        
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        raise

# Initialize database on startup
init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    """Add a new expense to the database"""
    try:
        with sqlite3.connect(DB_PATH, timeout=10) as conn:
            conn.isolation_level = None  # autocommit mode
            cur = conn.execute(
                "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
                (date, amount, category, subcategory, note)
            )
            conn.commit()
            
            return {
                'status': "ok", 
                "id": cur.lastrowid,
                "message": f"Expense of {amount} for {category} added successfully"
            }
    except sqlite3.OperationalError as e:
        return {'status': "error", "message": str(e)}

@mcp.tool()
def list_expenses():
    """Retrieve all expenses from the database"""
    try:
        with sqlite3.connect(DB_PATH, timeout=10) as conn:
            conn.isolation_level = None
            cur = conn.execute("SELECT id, date, amount, category, subcategory, note FROM expenses ORDER BY id ASC")
            cols = [d[0] for d in cur.description]
            expenses = [dict(zip(cols, r)) for r in cur.fetchall()]
            
            return {
                'status': 'ok',
                'count': len(expenses),
                'expenses': expenses
            }
    except sqlite3.OperationalError as e:
        return {'status': "error", "message": str(e)}

# Start Server
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

# to run == uv run main.py
# to inspect == uv run fastmcp dev inspector main.py