# infrastructure/interfaces/file_system_source.py

from abc import ABC, abstractmethod
from typing import List


class FileSystemSource(ABC):
    @abstractmethod
    def walk_directory(self, path: str) -> List[str]:
        """Returns a list of all absolute file paths in the directory."""
        pass

    @abstractmethod
    def read_file(self, path: str) -> str:
        """Returns the UTF-8 content of the file."""
        pass
