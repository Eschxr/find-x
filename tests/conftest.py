""" Shared test suite fixtures """

import shutil
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    """ Makes a fresh temp copy of tests/fixtures/sample_repo for each test """
    dest = tmp_path / "sample_repo"
    shutil.copytree(FIXTURES_DIR / "sample_repo", dest)
    return dest
