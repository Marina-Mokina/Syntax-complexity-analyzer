import sqlite3
from pathlib import Path


def find_postcard_in_corpus(text: str) -> dict:
    """
    Searches for a postcard by text in an existing database.

    Args:
    text: postcard text to search for
    db_path: path to the database containing the corpus

    Returns:
    dict: {'found': bool, 'id': int, 'date': str, 'tag': str} or None
    """
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent
    db_path = project_root / 'data' / 'corpus.db'

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            "id" as id,
            "date" as date,
            "tag" as tag,
            "text" as full_text
        FROM postcards 
        WHERE "text" LIKE ? 
    """, (f"%{text}%",))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            'id': result['id'],
            'date': result['date'],
            'tag': result['tag'],
        }
