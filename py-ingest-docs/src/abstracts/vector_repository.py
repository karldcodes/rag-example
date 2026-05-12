from abc import ABC, abstractmethod
import src.models as models

class VectorRepository:
    @abstractmethod
    def add(self, entry: models.VectorEntry) -> None:
        pass
