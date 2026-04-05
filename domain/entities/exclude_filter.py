# domain/entities/exclude_filter.py
from dataclasses import dataclass
from typing import List

from domain.entities.exclude_filter_rule import ExcludeFilterRule


@dataclass(frozen=True)
class ExcludeFilter:
    """
    Immutable entity that aggregates multiple filtering rules.
    If ANY rule returns True, the file is excluded.
    """

    rules: List[ExcludeFilterRule]

    def should_exclude(self, file_path: str) -> bool:
        """Evaluates all rules. Returns True if the path should be ignored."""
        return any(rule.should_exclude(file_path) for rule in self.rules)
