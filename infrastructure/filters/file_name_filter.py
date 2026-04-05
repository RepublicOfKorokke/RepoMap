import fnmatch

from domain.entities.exclude_filter_rule import ExcludeFilterRule


class FileNameExcludeFilter(ExcludeFilterRule):
    """Implements filtering using glob patterns."""

    def __init__(self, patterns: list[str]):
        self.patterns = patterns

    def should_exclude(self, file_path: str) -> bool:
        for pattern in self.patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        return False
