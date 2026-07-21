""" Embeds chunks into vectors 

Stubbed: Implement with sentence-transformers later
"""

from __future__ import annotations

import numpy as np

from find_x.core.models import CodeChunk

EMBEDDING_DIM = 384     # matches all-MiniLM-L6-v2


def embed_chunks(chunks: list[CodeChunk]) -> np.ndarray:
    return np.zeros((len(chunks), EMBEDDING_DIM), dtype=np.float32)


def embed_query(text: str) -> np.ndarray:
    return np.zeros(EMBEDDING_DIM, dtype=np.float32)
