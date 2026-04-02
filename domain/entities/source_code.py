# domain/entities/source_code.py
from dataclasses import dataclass


@dataclass(frozen=True)
class SourceCode:
    file_path: str
    content: str
    language_name: str

    def __post_init__(self):
        # DbC: Ensure basic preconditions for domain logic
        if not self.file_path:
            raise ValueError("File path is required.")
