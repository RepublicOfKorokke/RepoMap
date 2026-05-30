import fnmatch

from domain.entities.exclude_filter_rule import ExcludeFilterRule


class FileNameExcludeFilter(ExcludeFilterRule):
    def __init__(self, patterns: list[str], is_whitelist: bool):
        self.patterns = patterns
        self.is_whitelist = is_whitelist

    def should_exclude(self, file_path: str) -> bool:
        if not self.patterns:
            return False

        matched = any(fnmatch.fnmatch(file_path, p) for p in self.patterns)

        if self.is_whitelist:
            return not matched
        else:
            return matched
