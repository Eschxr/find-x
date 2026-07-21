""" Naive line-window chunking

Every parser exposes a `chunk(path, repo_root) -> list[CodeChunk]`
function with this exact signature
"""

from __future__ import annotations
from pathlib import Path

from find_x.core.models import CodeChunk
from find_x.core.scanner import language_for

WINDOW_SIZE = 40
OVERLAP = 5


def chunk(path: Path, repo_root: Path) -> list[CodeChunk]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    if not lines:
        return []

    rel_path = str(path.relative_to(repo_root))
    language = language_for(path)
    step = WINDOW_SIZE - OVERLAP

    chunks: list[CodeChunk] = []
    start = 0
    while start < len(lines):
        end = min(start + WINDOW_SIZE, len(lines))
        content = "\n".join(lines[start:end])
        start_line, end_line = start + 1, end

        chunks.append(
            CodeChunk(
                id=CodeChunk.compute_id(rel_path, start_line, end_line),
                repo_relative_path=rel_path,
                language=language,
                chunk_type="line_range",
                start_line=start_line,
                end_line=end_line,
                content=content,
            )
        )

        if end == len(lines):
            break
        start += step

    return chunks
