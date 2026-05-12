from src.abstracts.vector_repository import VectorRepository
from src.models.vector_entry import VectorEntry
from src.domain.text_file_reader import TextFileReader
from src.abstracts.text_chunker import TextChunker
from src.abstracts.embedding_provider import EmbeddingProvider
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)

class IngestDocuments:
    def __init__(self, embedding_provider: EmbeddingProvider, 
                 chunker: TextChunker, 
                 vector_repo: VectorRepository,
                 file_reader: TextFileReader):
        self.embedding_provider = embedding_provider
        self.chunker = chunker
        self.vector_repo = vector_repo
        self.file_reader = file_reader

    def start(self):
        logger.info("Starting document ingestion")
        for file in self.file_reader.get_files():
            text_file = self.file_reader.read(file=file)
            logger.info("file: %s", text_file.name)

            chunks = self.chunker.chunk_text(text_file.text)
            logger.info("Number of chunks: %s", str(len(chunks)))

            for chunk in chunks:
                embedding = self.embedding_provider.generate_embedding(chunk)
                self.vector_repo.add(VectorEntry(file_name=text_file.name, chunk=chunk, embedding=embedding))

            logger.info("Created embeddings for file")
        logger.info("Document ingestion complete")