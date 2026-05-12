from abc import ABC, abstractmethod

class TextChunker:
    @abstractmethod
    def chunk_text(self, text) -> list[str]:
        pass