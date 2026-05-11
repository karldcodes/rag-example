import os
from pathlib import Path
import psycopg
from langchain_text_splitters import CharacterTextSplitter
import getpass


# check we have all the env vars we need
if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:password@postgres:5432/rag_db"
)


def chunk_text(text):
    # Implement a hard constraint on the chunk size based on the model being used later for queries
    # in our case the c# project
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-5-nano",
        chunk_size=100, 
        chunk_overlap=0
    )
    # Split the text into fixed-size chunks
    return text_splitter.split_text(text)


def get_embedding_provider():
    # can be changed at will with out affecting code
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return embeddings


def main():
    print("Starting document ingestion")
    # creat embedding object
    embeddings = get_embedding_provider()

    docs_dir = Path("docs")
    # connect to vector db to store encoddings
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            for file in docs_dir.glob("*.txt"):
                print(f"Working on: {file.name}")
                # as the text is small read the whole file into memory. we could read it line by line for large files
                text = file.read_text(encoding="utf-8")
                # split document into chunks
                chunks = chunk_text(text)
                print(f"Number of chunks: {len(chunks)}")

                for chunk in chunks:
                    # generate text embedding from chunk
                    embedding = embeddings.embed_query(chunk)
                    cur.execute(
                            """
                            INSERT INTO document_chunks (source, content, embedding)
                            VALUES (%s, %s, %s)
                            """,
                            (file.name, chunk, embedding)
                        )
                print("Created embeddings for file")

        conn.commit()
    print("Document ingestion complete")


if __name__ == "__main__":
    main()