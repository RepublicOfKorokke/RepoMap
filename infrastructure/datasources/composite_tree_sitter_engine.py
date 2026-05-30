import logging
from typing import Dict, List

from infrastructure.dtos.raw_capture_dto import RawCaptureDto
from infrastructure.interfaces.tree_sitter_engine import TreeSitterEngine


class CompositeTreeSitterEngine(TreeSitterEngine):
    def __init__(
        self,
        default_engine: TreeSitterEngine,
        language_engines: Dict[str, TreeSitterEngine],
    ):
        self._logger = logging.getLogger(__name__)
        self._default_engine = default_engine
        self._language_engines = language_engines

    def parse_and_query(self, code: str, language_name: str) -> List[RawCaptureDto]:
        engine = self._language_engines.get(language_name.lower(), self._default_engine)
        self._logger.debug(f"Routing {language_name} to {engine.__class__.__name__}")

        return engine.parse_and_query(code, language_name)
