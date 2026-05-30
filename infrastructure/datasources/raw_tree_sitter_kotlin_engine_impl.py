import logging
from typing import List

from tree_sitter import Parser, QueryCursor
from tree_sitter_language_pack import get_language

from infrastructure.dtos.raw_capture_dto import RawCaptureDto
from infrastructure.interfaces.tree_sitter_engine import TreeSitterEngine


class RawTreeSitterKotlinEngineImpl(TreeSitterEngine):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

        self._language = get_language("kotlin")
        self._parser = Parser(self._language)

        self._query_string = """
        (object_declaration (type_identifier) @name.definition.object) @definition.object
        (class_declaration (type_identifier) @name.definition.class) @definition.class
        (function_declaration (simple_identifier) @name.definition.function) @definition.function
        (import_header (identifier) @name.reference.import)
        """
        self._query = self._language.query(self._query_string)

    def parse_and_query(self, code: str, language_name: str) -> List[RawCaptureDto]:
        if not code or language_name.lower() != "kotlin":
            return []

        try:
            self._logger.debug("Parsing Kotlin code with raw tree-sitter")

            tree = self._parser.parse(bytes(code, "utf-8"))
            cursor = QueryCursor(self._query)
            captures = cursor.captures(tree.root_node)

            raw_captures = []

            for capture_name, nodes in captures.items():
                for node in nodes:
                    if "name.definition" in capture_name:
                        capture_type = self.CAPTURE_TYPE_DEFINITION
                    elif "name.reference" in capture_name:
                        capture_type = self.CAPTURE_TYPE_REFERENCE
                    else:
                        continue

                    name = node.text.decode("utf-8") if node.text else ""
                    node_kind = capture_name.split(".")[-1]

                    start_line_num = node.start_point[0] + 1
                    end_line_num = node.end_point[0] + 1

                    if capture_type == self.CAPTURE_TYPE_DEFINITION and node.parent:
                        start_line_num = node.parent.start_point[0] + 1
                        end_line_num = node.parent.end_point[0] + 1

                    raw_captures.append(
                        RawCaptureDto(
                            node_text=name,
                            node_kind=node_kind,
                            capture_type=capture_type,
                            start_line=start_line_num,
                            end_line=end_line_num,
                        )
                    )

            return raw_captures

        except Exception as e:
            self._logger.error(f"Error parsing Kotlin code: {e}")
            return []
