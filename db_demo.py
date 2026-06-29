from __future__ import annotations
from sqlalchemy import text
from database import engine, init_db

def run_sql(query: str):
    """
    Run a raw SQL query on the same DB used by 'database.py'

    Example: 
        rows = run_sql("SELECT * FROM appointments")
        print(rows)
    """

    # init_db()   # Ensure that the db
    
    with engine.begin() as conn:
        result = conn.execute(text(query))
        return result.fetchall() if result.returns_rows else result.rowcount
    

# query = """INSERT into appointments (patient_name, reason, start_time, cancelled, created_at) VALUES ('John Doe', 'Routine Checkup', '2026-06-27 17:00:00', 0, datetime('now'))"""
query = "SELECT * FROM appointments"
print(run_sql(query))