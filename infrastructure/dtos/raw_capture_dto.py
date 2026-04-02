# infrastructure/dtos/raw_capture_dto.py
from dataclasses import dataclass


@dataclass(frozen=True)
class RawCaptureDto:
    """Pure data structure representing a raw Tree-sitter query match."""

    node_text: str
    node_kind: str
    capture_type: str  # def | ref
    start_line: int
    end_line: int
