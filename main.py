# main.py
import argparse
import logging

from domain.entities.exclude_filter import ExcludeFilter
from domain.usecases.parse_directory_usecase import ParseDirectoryUseCase
from infrastructure.analyzers.tree_sitter_syntax_analyzer_impl import (
    TreeSitterSyntaxAnalyzerImpl,
)
from infrastructure.datasources.local_file_system_source import LocalFileSystemSource
from infrastructure.datasources.tree_sitter_engine_impl import (
    TreeSitterEngineImpl,
)
from infrastructure.filters.file_name_filter import FileNameExcludeFilter
from infrastructure.repositories.local_source_code_repository import (
    LocalSourceCodeRepository,
)
from presentation.cli_view import CLIView


def main():
    # Configure logging
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Parse directory for code tags")
    parser.add_argument("directory_path", help="Directory path to parse")
    parser.add_argument(
        "--exclude",
        "-e",
        nargs="*",
        help="File patterns to exclude (e.g., *.py, *.log, __pycache__)",
    )
    args = parser.parse_args()

    target_directory = args.directory_path
    exclude_patterns = args.exclude if args.exclude else []

    logger.info(f"Starting parsing process for directory: {target_directory}")
    logger.info(f"Exclude patterns: {exclude_patterns}")

    # --- 1. Instantiate Data Sources & Filters ---
    logger.info("Instantiating data sources and filters...")
    file_system = LocalFileSystemSource()
    tree_sitter_engine = TreeSitterEngineImpl()

    file_name_rule = FileNameExcludeFilter(exclude_patterns)
    exclude_filter = ExcludeFilter(rules=[file_name_rule])

    # --- 2. Inject Data Sources into Interfaces ---
    logger.info("Injecting data sources into repositories and analyzers...")
    repository = LocalSourceCodeRepository(file_system_source=file_system)
    analyzer = TreeSitterSyntaxAnalyzerImpl(tree_sitter_engine=tree_sitter_engine)

    # --- 3. Inject Interfaces into Domain UseCase ---
    logger.info("Injecting interfaces into UseCase...")
    use_case = ParseDirectoryUseCase(repository=repository, analyzer=analyzer)

    # --- 4. Inject UseCase & FileSystem into Presentation View ---
    logger.info("Injecting UseCase and filters into CLI View...")
    cli_view = CLIView(
        use_case=use_case,
        file_system=file_system,
        exclude_filter=exclude_filter,
    )

    # --- 5. Execute Program ---
    logger.info("Executing parsing...")
    cli_view.start_parsing(target_directory)
    logger.info("Parsing process completed.")


if __name__ == "__main__":
    main()
