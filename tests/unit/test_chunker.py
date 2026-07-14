"""Tests for find_x.core.chunker.

Deliberately doesn't re-test line_based's boundary math (that's
test_line_based.py's job) - this only tests that the dispatcher routes
correctly and aggregates across multiple files.
"""

from find_x.core.chunker import chunk_file, chunk_repo
from find_x.core.scanner import scan_repo


def test_chunk_file_delegates_to_line_based(sample_repo):
    path = sample_repo / "small_module.py"
    chunks = chunk_file(path, sample_repo)
    assert len(chunks) == 1


def test_chunk_repo_aggregates_chunks_from_all_files(sample_repo):
    files = scan_repo(sample_repo)
    chunks = chunk_repo(files, sample_repo)

    paths_represented = {c.repo_relative_path for c in chunks}
    assert "small_module.py" in paths_represented
    assert "large_module.py" in paths_represented
    # empty_module.py contributes zero chunks but shouldn't break the pass
    assert "empty_module.py" not in paths_represented


def test_chunk_repo_with_no_files_returns_empty_list():
    assert chunk_repo([], repo_root=None) == []
