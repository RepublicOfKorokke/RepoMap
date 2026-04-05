# domain/usecases/parse_directory_usecase.py
from typing import Callable, List

from domain.entities.exclude_filter import ExcludeFilter
from domain.interfaces.source_code_repository import SourceCodeRepository
from domain.interfaces.syntax_analyzer import SyntaxAnalyzer
from domain.states.parsing_state import Error, Idle, ParsingState, Processing, Success


class ParseDirectoryUseCase:
    def __init__(self, repository: SourceCodeRepository, analyzer: SyntaxAnalyzer):
        self._repository = repository
        self._analyzer = analyzer
        self._state: ParsingState = Idle()
        self._subscribers: List[Callable[[ParsingState], None]] = []

    def subscribe(self, callback: Callable[[ParsingState], None]) -> None:
        self._subscribers.append(callback)
        callback(self._state)

    def _emit(self, new_state: ParsingState) -> None:
        self._state = new_state
        for callback in self._subscribers:
            callback(self._state)

    def execute(self, directory_path: str, exclude_filter: ExcludeFilter) -> None:
        """Orchestrates the directory parsing business process."""
        # DbC: Guard clause
        if not directory_path.strip():
            self._emit(Error("Directory path cannot be empty."))
            return

        self._emit(Processing())

        try:
            # 1. Fetch code entities
            source_codes = self._repository.fetch_target_codes(
                directory_path, exclude_filter
            )

            # 2. Aggregate tags
            all_tags = []
            for source in source_codes:
                tags = self._analyzer.analyze(source)
                all_tags.extend(tags)

            # 3. Complete process
            self._emit(Success(tags=all_tags))

        except Exception as e:
            # Domain Boundary: Catch unexpected infrastructure or logic errors
            self._emit(Error(message=f"Parsing failed: {str(e)}"))
