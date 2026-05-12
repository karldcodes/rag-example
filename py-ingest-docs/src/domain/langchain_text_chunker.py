from langchain_text_splitters import CharacterTextSplitter
from src.abstracts.text_chunker import TextChunker

class LangChainTextChunker(TextChunker):
    def __init__(self, model="gpt-5-nano", chunk_size=100, overlap=0):
        # Implement a hard constraint on the chunk size based on the model being used later for queries
        self.text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            model_name=model,
            chunk_size=chunk_size, 
            chunk_overlap=overlap
        )

    def chunk_text(self, text):
        return self.text_splitter.split_text(text)