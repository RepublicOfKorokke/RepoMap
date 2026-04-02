# domain/interfaces/syntax_analyzer.py
from abc import ABC, abstractmethod
from typing import List

from domain.entities.code_tag import CodeTag
from domain.entities.source_code import SourceCode


class SyntaxAnalyzer(ABC):
    @abstractmethod
    def analyze(self, source: SourceCode) -> List[CodeTag]:
        """Parses source code and extracts domain tags."""
        pass
