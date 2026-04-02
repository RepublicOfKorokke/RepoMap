# main.py
import sys

from domain.usecases.parse_directory_usecase import ParseDirectoryUseCase
from infrastructure.analyzers.tree_sitter_syntax_analyzer_impl import (
    TreeSitterSyntaxAnalyzerImpl,
)
from infrastructure.datasources.local_file_system_source import LocalFileSystemSource
from infrastructure.datasources.tree_sitter_engine_impl import (
    TreeSitterEngineImpl,
)
from infrastructure.repositories.local_source_code_repository import (
    LocalSourceCodeRepository,
)
from presentation.cli_view import CLIView


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]

    # --- 1. Instantiate Data Sources ---
    file_system = LocalFileSystemSource()
    tree_sitter_engine = TreeSitterEngineImpl()

    # --- 2. Inject Data Sources into Interfaces ---
    repository = LocalSourceCodeRepository(file_system_source=file_system)
    analyzer = TreeSitterSyntaxAnalyzerImpl(tree_sitter_engine=tree_sitter_engine)

    # --- 3. Inject Interfaces into Domain UseCase ---
    use_case = ParseDirectoryUseCase(repository=repository, analyzer=analyzer)

    # --- 4. Inject UseCase & FileSystem into Presentation View ---
    cli_view = CLIView(use_case=use_case, file_system=file_system)

    # --- 5. Execute Program ---
    cli_view.start_parsing(target_directory)


if __name__ == "__main__":
    main()
