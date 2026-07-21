""" Scans a repository & yields source files for chunking

Currently very limited in terms of allowed & disallowed extensions
and no .gitignore parsing (TODO later, just maps/sets for now)
"""

from __future__ import annotations
from pathlib import Path

LANGUAGE_BY_EXTENSION: dict[str, str] = {
    ".py": "python",
}

_IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".repo-explorer-data"}


def _is_ignored(path: Path) -> bool:
    return any(part in _IGNORED_DIRS for part in path.parts)


def scan_repo(repo_root: Path) -> list[Path]:
    """ Return list of abs paths to all scannable files under repo_root """
    repo_root = repo_root.resolve()
    files: list[Path] = []
    for ext in LANGUAGE_BY_EXTENSION:
        for path in repo_root.rglob(f"*{ext}"):
            if path.is_file() and not _is_ignored(path.relative_to(repo_root)):
                files.append(path)
    return sorted(files)


def language_for(path: Path) -> str:
    return LANGUAGE_BY_EXTENSION.get(path.suffix, "unknown")
