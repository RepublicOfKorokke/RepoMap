# domain/interfaces/source_code_repository.py
from abc import ABC, abstractmethod
from typing import List

from domain.entities.source_code import SourceCode


class SourceCodeRepository(ABC):
    @abstractmethod
    def fetch_target_codes(self, directory_path: str) -> List[SourceCode]:
        """Retrieves source code entities from a directory path."""
        pass
