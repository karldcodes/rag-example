from langchain_openai import OpenAIEmbeddings
from src.abstracts.embedding_provider import EmbeddingProvider

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model="text-embedding-3-small"):        
        embeddings = OpenAIEmbeddings(model=model)
        self.embeddings = embeddings

    def generate_embedding(self, chunk):
        return self.embeddings.embed_query(chunk)