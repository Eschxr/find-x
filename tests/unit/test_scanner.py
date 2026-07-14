"""Tests for find_x.core.scanner."""

from pathlib import Path

from find_x.core.scanner import language_for, scan_repo


def relative_paths(repo_root: Path) -> set[str]:
    return {str(p.relative_to(repo_root)) for p in scan_repo(repo_root)}


def test_finds_all_python_files_including_nested(sample_repo):
    found = relative_paths(sample_repo)
    assert "small_module.py" in found
    assert "large_module.py" in found
    assert "empty_module.py" in found
    assert str(Path("pkg") / "__init__.py") in found
    assert str(Path("pkg") / "nested.py") in found


def test_excludes_non_python_files(sample_repo):
    found = relative_paths(sample_repo)
    assert "README.md" not in found


def test_excludes_ignored_directories(sample_repo):
    found = relative_paths(sample_repo)
    assert not any("__pycache__" in path for path in found)


def test_returns_absolute_sorted_paths(sample_repo):
    files = scan_repo(sample_repo)
    assert all(p.is_absolute() for p in files)
    assert files == sorted(files)


def test_accepts_unresolved_relative_root(sample_repo, monkeypatch):
    # scan_repo resolves internally - a caller passing "." shouldn't break it
    monkeypatch.chdir(sample_repo)
    files = scan_repo(Path("."))
    assert any(p.name == "small_module.py" for p in files)


def test_empty_directory_returns_no_files(tmp_path):
    assert scan_repo(tmp_path) == []


def test_language_for_known_and_unknown_extensions():
    assert language_for(Path("foo.py")) == "python"
    assert language_for(Path("README.md")) == "unknown"
    assert language_for(Path("no_extension")) == "unknown"
