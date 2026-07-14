"""Tests for find_x.core.embedder.

These test the *shape contract* the stub already guarantees (dimension,
dtype, one row per chunk) - the values are meaningless placeholders until
Phase 4 swaps in a real model, but the contract itself is real and worth
locking in now so Phase 4's implementation has to satisfy the same shape.
"""

import numpy as np

from find_x.core.embedder import EMBEDDING_DIM, embed_chunks, embed_query
from find_x.core.models import CodeChunk


def make_chunk(n: int) -> CodeChunk:
    return CodeChunk(
        id=CodeChunk.compute_id(f"file_{n}.py", 1, 1),
        repo_relative_path=f"file_{n}.py",
        language="python",
        chunk_type="line_range",
        start_line=1,
        end_line=1,
        content="pass",
    )


def test_embed_chunks_returns_one_row_per_chunk():
    chunks = [make_chunk(i) for i in range(3)]
    embeddings = embed_chunks(chunks)
    assert embeddings.shape == (3, EMBEDDING_DIM)


def test_embed_chunks_with_empty_list_returns_empty_array():
    embeddings = embed_chunks([])
    assert embeddings.shape == (0, EMBEDDING_DIM)


def test_embed_chunks_returns_float32():
    embeddings = embed_chunks([make_chunk(0)])
    assert embeddings.dtype == np.float32


def test_embed_query_returns_single_vector_of_correct_dimension():
    embedding = embed_query("how are chunks embedded")
    assert embedding.shape == (EMBEDDING_DIM,)
    