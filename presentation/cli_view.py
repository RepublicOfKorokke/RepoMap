# presentation/cli_view.py

import os
from collections import defaultdict

from domain.entities.code_tag import CodeTag
from domain.entities.tag_kind import TagKind
from domain.states.parsing_state import Error, Idle, ParsingState, Processing, Success
from domain.usecases.parse_directory_usecase import ParseDirectoryUseCase
from infrastructure.interfaces.file_system_source import FileSystemSource


class CLIView:
    def __init__(self, use_case: ParseDirectoryUseCase, file_system: FileSystemSource):
        self._use_case = use_case
        self._file_system = file_system
        self._use_case.subscribe(self._on_state_changed)

    def _on_state_changed(self, state: ParsingState) -> None:
        if isinstance(state, Idle):
            pass

        elif isinstance(state, Processing):
            print("\n[INFO] Scanning directory and analyzing syntax trees...\n")

        elif isinstance(state, Success):
            self._render_simple_format(state.tags)

        elif isinstance(state, Error):
            print("\n[ERROR] A failure occurred during processing:")
            print(f">>> {state.message}\n")

    def _render_simple_format(self, tags: list[CodeTag]) -> None:
        if not tags:
            print("No tags found.")
            return

        file_map: dict = defaultdict(lambda: {"defs": [], "refs": set()})

        for tag in tags:
            rel_path = os.path.relpath(tag.file_path, os.getcwd())
            if tag.tag_kind == TagKind.DEF:
                file_map[rel_path]["defs"].append(tag)
            elif tag.tag_kind == TagKind.REF:
                file_map[rel_path]["refs"].add(tag.identifier_name)

        for file_path, data in file_map.items():
            print(f"📦 {file_path}")

            if len(data["refs"]) > 0:
                print("   Dependencies:")
                for ref in data["refs"]:
                    print(f"      {ref}")

            if len(data["defs"]) > 0:
                print("   Definitions:")
                for tag in sorted(data["defs"], key=lambda x: x.start_line):
                    print(
                        f"      [L{tag.start_line}-{tag.end_line}] {tag.identifier_type} {tag.identifier_name}"
                    )

            print()

    def start_parsing(self, directory_path: str) -> None:

        self._use_case.execute(directory_path)
