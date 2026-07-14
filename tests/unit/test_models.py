"""Tests for find_x.core.models.

Covers: ID determinism (the thing incremental reindexing depends on),
range validation, computed fields, JSON round-tripping, and score
aggregation on SearchResult.
"""

import pytest
from pydantic import ValidationError

from find_x.core.models import CodeChunk, Query, SearchResult


def make_chunk(**overrides) -> CodeChunk:
    """Small factory so each test only states the fields it cares about."""
    defaults = dict(
        repo_relative_path="pkg/nested.py",
        language="python",
        chunk_type="line_range",
        start_line=1,
        end_line=10,
        content="class Widget:\n    pass",
    )
    defaults.update(overrides)
    defaults["id"] = CodeChunk.compute_id(
        defaults["repo_relative_path"], defaults["start_line"], defaults["end_line"]
    )
    return CodeChunk(**defaults)


# --- compute_id -------------------------------------------------------


def test_compute_id_is_deterministic():
    id_a = CodeChunk.compute_id("pkg/nested.py", 1, 10)
    id_b = CodeChunk.compute_id("pkg/nested.py", 1, 10)
    assert id_a == id_b


@pytest.mark.parametrize(
    "path_a, start_a, end_a, path_b, start_b, end_b",
    [
        # different path, same range
        ("pkg/nested.py", 1, 10, "pkg/other.py", 1, 10),
        # same path, different start
        ("pkg/nested.py", 1, 10, "pkg/nested.py", 2, 10),
        # same path, different end
        ("pkg/nested.py", 1, 10, "pkg/nested.py", 1, 11),
    ],
)
def test_compute_id_differs_when_inputs_differ(path_a, start_a, end_a, path_b, start_b, end_b):
    id_a = CodeChunk.compute_id(path_a, start_a, end_a)
    id_b = CodeChunk.compute_id(path_b, start_b, end_b)
    assert id_a != id_b


# --- range validation ---------------------------------------------------


def test_inverted_range_raises_validation_error():
    with pytest.raises(ValidationError, match="start_line"):
        make_chunk(start_line=20, end_line=10)


def test_single_line_chunk_is_valid():
    # start_line == end_line is a valid one-line chunk, not an error
    chunk = make_chunk(start_line=5, end_line=5)
    assert chunk.line_count == 1


# --- computed fields ------------------------------------------------------


@pytest.mark.parametrize(
    "start_line, end_line, expected_count",
    [
        (1, 10, 10),
        (1, 1, 1),
        (36, 75, 40),
    ],
)
def test_line_count(start_line, end_line, expected_count):
    chunk = make_chunk(start_line=start_line, end_line=end_line)
    assert chunk.line_count == expected_count


def test_metadata_defaults_to_empty_dict():
    chunk = make_chunk()
    assert chunk.metadata == {}


# --- serialization ---------------------------------------------------------


def test_json_round_trip_preserves_data():
    original = make_chunk(metadata={"function_name": "render"})
    restored = CodeChunk.model_validate_json(original.model_dump_json())
    assert restored == original


def test_json_output_includes_computed_line_count():
    chunk = make_chunk(start_line=1, end_line=10)
    dumped = chunk.model_dump()
    assert dumped["line_count"] == 10


# --- SearchResult -----------------------------------------------------


def test_search_result_total_score_sums_all_score_components():
    result = SearchResult(chunk=make_chunk(), scores={"embedding": 0.7, "keyword": 0.2})
    assert result.total_score == pytest.approx(0.9)


def test_search_result_total_score_is_zero_with_no_scores():
    result = SearchResult(chunk=make_chunk())
    assert result.total_score == 0.0


# --- Query ---------------------------------------------------------------


def test_query_top_k_defaults_to_five():
    query = Query(text="how are chunks embedded")
    assert query.top_k == 5
