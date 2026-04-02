# infrastructure/interfaces/tree_sitter_engine.py
from abc import ABC, abstractmethod
from typing import List

from infrastructure.dtos.raw_capture_dto import RawCaptureDto


class TreeSitterEngine(ABC):
    CAPTURE_TYPE_DEFINITION = "definition"
    CAPTURE_TYPE_REFERENCE = "reference"

    @abstractmethod
    def parse_and_query(self, code: str, language_name: str) -> List[RawCaptureDto]:
        """Executes a syntax tree query and returns raw DTO captures."""
        pass
