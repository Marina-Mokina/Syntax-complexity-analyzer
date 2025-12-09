import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class CorpusSearch:
    """
    Searches for postcards in a corpus database by text content.
    """

    def __init__(self, text: str):
        """
        Initialize CorpusSearch with text to find.

        Args:
            text: Postcard text to search for in the corpus
        """
        self.text = text
        self.metadata = None

    def find_postcard_in_corpus(self) -> Optional[Dict[str, Any]]:
        """
        Search for a postcard by text in an existing database.

        Returns:
            Dictionary with postcard metadata if found, None otherwise.
            Metadata contains: 'id', 'date', 'tag'
        """
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        db_path = project_root / 'data' / 'corpus.db'

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                "id" as id,
                "date" as date,
                "tag" as tag,
                "text" as full_text
            FROM postcards 
            WHERE "text" LIKE ? 
            """,
            (f'%{self.text}%',),
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            self.metadata = {
                'id': result['id'],
                'date': result['date'],
                'tag': result['tag'],
            }
            logger.info(f"Found postcard: ID={self.metadata['id']}, "
                        f"Date={self.metadata['date']}, Tag={self.metadata['tag']}")
            return self.metadata

    def display_corpus_postcard(self) -> None:
        """
        Display information about found postcard.
        """
        if self.metadata:
            print(f'\nОткрытка найдена в корпусе')
            print(f'      Номер: #{self.metadata["id"]}')
            print(f'      Дата: {self.metadata["date"]}')
            print(f'      Тег: {self.metadata["tag"]}\n')
        else:
            print('Не найдено в корпусе')
