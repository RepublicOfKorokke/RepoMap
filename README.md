# About

A CLI tool for parsing source code files in a directory.
It analyzes codebases using TreeSitter to extract structured information from your source files.

# Feature

- Parses all code files in a given directory
- Supports exclusion patterns to skip unwanted file types (e.g., `*test*`, `*.py`)
- Uses TreeSitter for accurate syntax analysis and code capture

# Usage

First of all, you need to run `uv sync` once before use this repo.

To parse a directory:

```bash
uv run main.py .

# or use wrapper shell script
repomap.sh .
```

To exclude specific file patterns (e.g., skip cache and log files):

```bash
uv run main.py ./my_project --exclude "*test*" "*view*"

# or use wrapper shell script
repomap.sh . --exclude "*test*" "*view*"
```

<details>
<summary>Example output</summary>

```
# run repomap in this repository
$ repomap.sh .
## domain/entities/code_tag.py
- Dependencies:
  - from domain.entities.tag_kind import TagKind
  - from dataclasses import dataclass
- Definitions:
  - [L7-30] CodeTag Class
  - [L15-30] __post_init__ Function

## domain/entities/exclude_filter.py
- Dependencies:
  - from domain.entities.exclude_filter_rule import ExcludeFilterRule
  - from dataclasses import dataclass
  - from typing import List
- Definitions:
  - [L8-18] ExcludeFilter Class
  - [L16-18] should_exclude Function

## domain/entities/exclude_filter_rule.py
- Dependencies:
  - from abc import ABC, abstractmethod
- Definitions:
  - [L4-9] ExcludeFilterRule Class
  - [L8-9] should_exclude Function

## domain/entities/source_code.py
- Dependencies:
  - from dataclasses import dataclass
- Definitions:
  - [L5-13] SourceCode Class
  - [L10-13] __post_init__ Function

## domain/entities/tag_kind.py
- Dependencies:
  - from enum import Enum, auto
- Definitions:
  - [L3-5] TagKind Class

## domain/interfaces/source_code_repository.py
- Dependencies:
  - from domain.entities.source_code import SourceCode
  - from abc import ABC, abstractmethod
  - from domain.entities.exclude_filter import ExcludeFilter
  - from typing import List
- Definitions:
  - [L8-14] SourceCodeRepository Class
  - [L10-14] fetch_target_codes Function

## domain/interfaces/syntax_analyzer.py
- Dependencies:
  - from domain.entities.code_tag import CodeTag
  - from abc import ABC, abstractmethod
  - from domain.entities.source_code import SourceCode
  - from typing import List
- Definitions:
  - [L8-12] SyntaxAnalyzer Class
  - [L10-12] analyze Function

## domain/states/parsing_state.py
- Dependencies:
  - from domain.entities.code_tag import CodeTag
  - from dataclasses import dataclass
  - from typing import List
- Definitions:
  - [L8-9] ParsingState Class
  - [L13-14] Idle Class
  - [L18-19] Processing Class
  - [L23-24] Success Class
  - [L28-29] Error Class

## domain/usecases/parse_directory_usecase.py
- Dependencies:
  - from domain.interfaces.source_code_repository import SourceCodeRepository
  - from domain.states.parsing_state import Error, Idle, ParsingState, Processing, Success
  - from domain.entities.exclude_filter import ExcludeFilter
  - from domain.interfaces.syntax_analyzer import SyntaxAnalyzer
  - from typing import Callable, List
- Definitions:
  - [L9-51] ParseDirectoryUseCase Class
  - [L10-14] __init__ Function
  - [L16-18] subscribe Function
  - [L20-23] _emit Function
  - [L25-51] execute Function

## infrastructure/analyzers/tree_sitter_syntax_analyzer_impl.py
- Dependencies:
  - from domain.entities.source_code import SourceCode
  - from domain.entities.code_tag import CodeTag
  - from infrastructure.dtos.raw_capture_dto import RawCaptureDto
  - from domain.interfaces.syntax_analyzer import SyntaxAnalyzer
  - import logging
  - from domain.entities.tag_kind import TagKind
  - from infrastructure.interfaces.tree_sitter_engine import TreeSitterEngine
  - from typing import List
- Definitions:
  - [L12-46] TreeSitterSyntaxAnalyzerImpl Class
  - [L13-15] __init__ Function
  - [L17-29] analyze Function
  - [L31-46] _map_to_domain_tag Function

## infrastructure/datasources/local_file_system_source.py
- Dependencies:
  - import os
  - import subprocess
  - import logging
  - from infrastructure.interfaces.file_system_source import FileSystemSource
  - from typing import List
- Definitions:
  - [L8-56] LocalFileSystemSource Class
  - [L9-48] walk_directory Function
  - [L50-56] read_file Function

## infrastructure/datasources/tree_sitter_engine_impl.py
- Dependencies:
  - import os
  - from infrastructure.dtos.raw_capture_dto import RawCaptureDto
  - from tree_sitter_language_pack import (
        ProcessConfig,
        configure,
        get_language,
        process,
    )
  - import logging
  - from infrastructure.interfaces.tree_sitter_engine import TreeSitterEngine
  - from typing import List
- Definitions:
  - [L25-32] TreeSitterConstants Class
  - [L35-97] TreeSitterEngineImpl Class
  - [L36-37] __init__ Function
  - [L39-78] parse_and_query Function
  - [L80-97] _process_node Function

## infrastructure/dtos/raw_capture_dto.py
- Dependencies:
  - from dataclasses import dataclass
- Definitions:
  - [L5-12] RawCaptureDto Class

## infrastructure/filters/file_name_filter.py
- Dependencies:
  - from domain.entities.exclude_filter_rule import ExcludeFilterRule
  - import fnmatch
- Definitions:
  - [L5-15] FileNameExcludeFilter Class
  - [L8-9] __init__ Function
  - [L11-15] should_exclude Function

## infrastructure/interfaces/file_system_source.py
- Dependencies:
  - from abc import ABC, abstractmethod
  - from typing import List
- Definitions:
  - [L6-15] FileSystemSource Class
  - [L8-10] walk_directory Function
  - [L13-15] read_file Function

## infrastructure/interfaces/tree_sitter_engine.py
- Dependencies:
  - from abc import ABC, abstractmethod
  - from typing import List
  - from infrastructure.dtos.raw_capture_dto import RawCaptureDto
- Definitions:
  - [L7-14] TreeSitterEngine Class
  - [L12-14] parse_and_query Function

## infrastructure/repositories/local_source_code_repository.py
- Dependencies:
  - from domain.interfaces.source_code_repository import SourceCodeRepository
  - from tree_sitter_language_pack._native import detect_language
  - from domain.entities.source_code import SourceCode
  - from domain.entities.exclude_filter import ExcludeFilter
  - import logging
  - from infrastructure.interfaces.file_system_source import FileSystemSource
  - from typing import List
- Definitions:
  - [L17-49] LocalSourceCodeRepository Class
  - [L18-20] __init__ Function
  - [L22-49] fetch_target_codes Function

## main.py
- Dependencies:
  - from presentation.cli_view import CLIView
  - from infrastructure.filters.file_name_filter import FileNameExcludeFilter
  - from infrastructure.repositories.local_source_code_repository import (
    LocalSourceCodeRepository,
)
  - from infrastructure.datasources.tree_sitter_engine_impl import (
    TreeSitterEngineImpl,
)
  - from infrastructure.datasources.local_file_system_source import LocalFileSystemSource
  - from domain.usecases.parse_directory_usecase import ParseDirectoryUseCase
  - from domain.entities.exclude_filter import ExcludeFilter
  - import argparse
  - from infrastructure.analyzers.tree_sitter_syntax_analyzer_impl import (
    TreeSitterSyntaxAnalyzerImpl,
)
  - import logging
- Definitions:
  - [L20-72] main Function

## presentation/cli_view.py
- Dependencies:
  - from collections import defaultdict
  - import os
  - from domain.states.parsing_state import Error, Idle, ParsingState, Processing, Success
  - from domain.usecases.parse_directory_usecase import ParseDirectoryUseCase
  - from domain.entities.exclude_filter import ExcludeFilter
  - from domain.entities.code_tag import CodeTag
  - import logging
  - from domain.entities.tag_kind import TagKind
  - from infrastructure.interfaces.file_system_source import FileSystemSource
- Definitions:
  - [L14-75] CLIView Class
  - [L15-25] __init__ Function
  - [L27-41] _on_state_changed Function
  - [L43-72] _render_simple_format Function
  - [L74-75] start_parsing Function

```

</details>
