"""Tests for find_x.storage.base."""

import numpy as np
import pytest

from find_x.core.models import CodeChunk
from find_x.storage.base import EmptyVectorStore, VectorStore


def test_vectorstore_cannot_be_instantiated_directly():
    # It's an ABC - this is what guarantees future stores (numpy_store,
    # faiss_store) can't accidentally skip implementing add/search.
    with pytest.raises(TypeError):
        VectorStore()


def test_empty_vector_store_search_always_returns_empty_list():
    store = EmptyVectorStore()
    results = store.search(np.zeros(384), top_k=5)
    assert results == []


def test_empty_vector_store_add_does_not_raise():
    store = EmptyVectorStore()
    chunk = CodeChunk(
        id=CodeChunk.compute_id("a.py", 1, 1),
        repo_relative_path="a.py",
        language="python",
        chunk_type="line_range",
        start_line=1,
        end_line=1,
        content="pass",
    )
    store.add([chunk], np.zeros((1, 384)))  # should not raise
    