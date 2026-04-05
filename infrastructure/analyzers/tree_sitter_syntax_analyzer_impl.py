# infrastructure/analyzers/tree_sitter_syntax_analyzer_impl.py
import logging
from typing import List

from domain.entities.code_tag import CodeTag
from domain.entities.source_code import SourceCode
from domain.entities.tag_kind import TagKind
from domain.interfaces.syntax_analyzer import SyntaxAnalyzer
from infrastructure.dtos.raw_capture_dto import RawCaptureDto
from infrastructure.interfaces.tree_sitter_engine import TreeSitterEngine


class TreeSitterSyntaxAnalyzerImpl(SyntaxAnalyzer):
    def __init__(self, tree_sitter_engine: TreeSitterEngine):
        self._engine = tree_sitter_engine
        self._logger = logging.getLogger(__name__)

    def analyze(self, source: SourceCode) -> List[CodeTag]:
        self._logger.info(
            f"Analyzing source: {source.file_path} ({source.language_name})"
        )
        # 1. Delegate to the heavy-lifting engine
        raw_captures = self._engine.parse_and_query(
            source.content, source.language_name
        )

        # 2. DRY (Mapping): Convert Infrastructure DTOs to Domain Entities
        tags = [self._map_to_domain_tag(dto, source.file_path) for dto in raw_captures]
        self._logger.debug(f"Found {len(tags)} tags in {source.file_path}")
        return tags

    def _map_to_domain_tag(self, dto: RawCaptureDto, file_path: str) -> CodeTag:
        """Pure mapper function."""
        KIND_MAP = {
            TreeSitterEngine.CAPTURE_TYPE_DEFINITION: TagKind.DEF,
            TreeSitterEngine.CAPTURE_TYPE_REFERENCE: TagKind.REF,
        }
        kind = KIND_MAP.get(dto.capture_type, TagKind.REF)

        return CodeTag(
            identifier_name=dto.node_text,
            identifier_type=dto.node_kind,
            tag_kind=kind,
            file_path=file_path,
            start_line=dto.start_line,
            end_line=dto.end_line,
        )
