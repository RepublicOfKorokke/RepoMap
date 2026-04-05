#!/usr/bin/env bash

# Wrapper script to run the parsing tool with the repo's .venv

set -e

SCRIPT_DIR="$(cd $(dirname $(realpath ${BASH_SOURCE[0]})) && pwd)"
TARGET_DIR="${1:-.}"

if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Error: .venv virtual environment not found."
    echo "Run 'uv sync' to create it."
    exit 1
fi

uv run --project "${SCRIPT_DIR}" "${SCRIPT_DIR}/main.py" "$TARGET_DIR"
