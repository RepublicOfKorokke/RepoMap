import logging
import os
import subprocess
from typing import List

from infrastructure.interfaces.file_system_source import FileSystemSource


class LocalFileSystemSource(FileSystemSource):
    def walk_directory(self, path: str) -> List[str]:
        logger = logging.getLogger(__name__)
        # DbC: Precondition validation
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found: {path}")

        try:
            logger.info(f"Attempting to walk directory using git: {path}")
            # Utilizes external infrastructure (Git) to obtain a list of files with strict .gitignore enforcement
            result = subprocess.run(
                ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                cwd=path,
                capture_output=True,
                text=True,
                check=True,
            )

            file_paths = []
            for line in result.stdout.splitlines():
                if line.strip():
                    # git ls-files returns relative paths; convert them to absolute paths
                    file_paths.append(os.path.abspath(os.path.join(path, line.strip())))

            logger.info(f"Successfully found {len(file_paths)} files via git.")
            return file_paths

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.warning(
                f"Git walk failed ({e}), falling back to os.walk for: {path}"
            )
            # Boundary Control: Fallback for cases where the path is not a Git repository or the Git command is unavailable
            file_paths = []
            for root, dirs, files in os.walk(path):
                # Exclude hidden directories (e.g., .git) from traversal
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                for file in files:
                    if not file.startswith("."):
                        file_paths.append(os.path.abspath(os.path.join(root, file)))
            logger.info(f"Found {len(file_paths)} files via os.walk.")
            return file_paths

    def read_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except (UnicodeDecodeError, PermissionError) as e:
            # Re-raise as a generic IO error for the repository to catch
            raise IOError(f"Could not read file {path}: {str(e)}")
