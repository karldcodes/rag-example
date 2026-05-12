
from src.domain.openai_embedding_provider import OpenAIEmbeddingProvider
from src.domain.ingest_documents import IngestDocuments
from src.domain.langchain_text_chunker import LangChainTextChunker
from src.domain.postgres_repository import PostgresRepository
from src.domain.text_file_reader import TextFileReader
from src.config import DATABASE_URL


def main():
    ingestor = IngestDocuments(embedding_provider=OpenAIEmbeddingProvider(), 
                               chunker=LangChainTextChunker(), 
                               vector_repo=PostgresRepository(DATABASE_URL),
                               file_reader=TextFileReader())
    ingestor.start()


if __name__ == "__main__":
    main()