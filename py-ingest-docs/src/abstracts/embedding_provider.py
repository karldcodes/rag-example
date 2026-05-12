from abc import ABC, abstractmethod

class EmbeddingProvider:
    @abstractmethod
    def generate_embedding(self, chunk) -> list[float]: 
        pass