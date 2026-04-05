# infrastructure/repositories/local_source_code_repository.py
from typing import List

from domain.entities.exclude_filter import ExcludeFilter  # 追加
from domain.entities.source_code import SourceCode
from domain.interfaces.source_code_repository import SourceCodeRepository
from infrastructure.interfaces.file_system_source import FileSystemSource

try:
    from tree_sitter_language_pack._native import detect_language
except ImportError as e:
    raise ImportError(
        f"Missing dependency: {e}. Run 'pip install tree-sitter-language-pack'"
    )


class LocalSourceCodeRepository(SourceCodeRepository):
    def __init__(self, file_system_source: FileSystemSource):
        self._file_system = file_system_source

    def fetch_target_codes(
        self, directory_path: str, exclude_filter: ExcludeFilter
    ) -> List[SourceCode]:
        try:
            paths = self._file_system.walk_directory(directory_path)
            sources: list[SourceCode] = []

            for path in paths:
                if exclude_filter.should_exclude(path):
                    continue

                lang = detect_language(path)

                if lang:
                    content = self._file_system.read_file(path)
                    sources.append(
                        SourceCode(file_path=path, content=content, language_name=lang)
                    )
            return sources
        except Exception as e:
            raise RuntimeError(f"Source repository failure: {str(e)}")
