""" Coordinates each file to the corresponding chunking strategy 

Everything uses line_based chunking for now, later will be a
language -> strategy map.
"""

from __future__ import annotations
from pathlib import Path

from find_x.core.models import CodeChunk
from find_x.parsers import line_based


def chunk_file(path: Path, repo_root: Path) -> list[CodeChunk]:
    return line_based.chunk(path, repo_root)


def chunk_repo(files: list[Path], repo_root: Path) -> list[CodeChunk]:
    chunks: list[CodeChunk] = []
    for path in files:
        chunks.extend(chunk_file(path, repo_root))
    return chunks
