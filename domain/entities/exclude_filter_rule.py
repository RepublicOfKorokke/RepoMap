# domain/entities/exclude_filter_rule.py
from abc import ABC, abstractmethod


class ExcludeFilterRule(ABC):
    """Abstract contract for filtering logic."""

    @abstractmethod
    def should_exclude(self, file_path: str) -> bool:
        pass
