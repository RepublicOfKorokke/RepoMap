# infrastructure/datasources/tree_sitter_engine_impl.py
import logging
import os
from typing import List

from infrastructure.dtos.raw_capture_dto import RawCaptureDto
from infrastructure.interfaces.tree_sitter_engine import TreeSitterEngine

try:
    from tree_sitter_language_pack import (
        ProcessConfig,
        configure,
        get_language,
        process,
    )

    configure(
        cache_dir=f"{os.path.dirname(os.path.abspath(__file__))}/tree_sitter_engines/"
    )
except ImportError as e:
    raise ImportError(
        f"Missing dependency: {e}. Run 'pip install tree-sitter-language-pack'"
    )


class TreeSitterConstants:
    STRUCTURE = "structure"
    IMPORTS = "imports"
    CHILDREN = "children"
    NODE_KIND_IMPORT = "import"
    SPAN = "span"
    START_LINE = "start_line"
    END_LINE = "end_line"


class TreeSitterEngineImpl(TreeSitterEngine):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def parse_and_query(self, code: str, language_name: str) -> List[RawCaptureDto]:
        if not code or not language_name:
            return []

        try:
            self._logger.debug(f"Parsing code with language: {language_name}")
            get_language(language_name)
            config = ProcessConfig(
                language=language_name,
            )

            result = process(code, config)

            raw_captures = []

            if TreeSitterConstants.STRUCTURE in result:
                for item in result[TreeSitterConstants.STRUCTURE]:
                    self._process_node(item, raw_captures)

            if TreeSitterConstants.IMPORTS in result:
                for imp in result[TreeSitterConstants.IMPORTS]:
                    raw_captures.append(
                        RawCaptureDto(
                            node_text=imp["source"],
                            node_kind=TreeSitterConstants.NODE_KIND_IMPORT,
                            capture_type=self.CAPTURE_TYPE_REFERENCE,
                            start_line=imp[TreeSitterConstants.SPAN][
                                TreeSitterConstants.START_LINE
                            ],
                            end_line=imp[TreeSitterConstants.SPAN][
                                TreeSitterConstants.END_LINE
                            ],
                        )
                    )

            return raw_captures

        except Exception as e:
            self._logger.error(f"Exception occurred in TreeSitterEngineImpl: {e}")
            return []

    def _process_node(self, node: dict, raw_captures: list[RawCaptureDto]):
        raw_captures.append(
            RawCaptureDto(
                node_text=node["name"],
                node_kind=node["kind"],
                capture_type=self.CAPTURE_TYPE_DEFINITION,
                start_line=node[TreeSitterConstants.SPAN][
                    TreeSitterConstants.START_LINE
                ],
                end_line=node[TreeSitterConstants.SPAN][TreeSitterConstants.END_LINE],
            )
        )

        if TreeSitterConstants.CHILDREN in node and isinstance(
            node[TreeSitterConstants.CHILDREN], list
        ):
            for child in node[TreeSitterConstants.CHILDREN]:
                self._process_node(child, raw_captures)
