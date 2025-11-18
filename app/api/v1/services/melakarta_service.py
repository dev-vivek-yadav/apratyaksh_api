import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create and return a new MySQL DB connection."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def fetch_all_ragas():
    """Fetch all Melakarta ragas from the DB."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM melakarta_ragas ORDER BY raga_number")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def fetch_raga_by_number(raga_number: int):
    """Fetch a single Melakarta raga by its number."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM melakarta_ragas WHERE raga_number = %s", (raga_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
