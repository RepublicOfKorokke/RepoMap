# domain/entities/code_tag.py
from dataclasses import dataclass

from domain.entities.tag_kind import TagKind


@dataclass(frozen=True)
class CodeTag:
    identifier_name: str
    identifier_type: str
    tag_kind: TagKind
    file_path: str
    start_line: int
    end_line: int

    def __post_init__(self):
        # DbC: Ensure basic preconditions for domain logic
        if not self.identifier_name.strip():
            raise ValueError("Identifier name cannot be empty.")
        if not self.identifier_type.strip():
            raise ValueError("Identifier type cannot be empty.")
        if self.start_line < 0:
            raise ValueError("Start line cannot be negative.")
        if self.end_line < 0:
            raise ValueError("End line cannot be negative.")
        if self.start_line > self.end_line:
            raise ValueError(
                f"start_line ({self.start_line}) cannot be greater than end_line ({self.end_line})."
            )
        if not isinstance(self.tag_kind, TagKind):
            raise ValueError("tag_kind must be an instance of TagKind.")
