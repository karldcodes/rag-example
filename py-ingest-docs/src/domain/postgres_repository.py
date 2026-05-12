from src.abstracts.vector_repository import VectorRepository
from src.models.vector_entry import VectorEntry
import psycopg


class PostgresRepository(VectorRepository):
    def __init__(self, db_url):
        self.conn = psycopg.connect(db_url)
        self.cur = self.conn.cursor()
    
    def add(self, entry: VectorEntry):
        self.cur.execute(
                        """
                        INSERT INTO document_chunks (source, content, embedding)
                        VALUES (%s, %s, %s)
                        """,
                        (entry.file_name, entry.chunk, entry.embedding)
                    )
        self.conn.commit()
