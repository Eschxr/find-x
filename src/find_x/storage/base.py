#src/find_x/storage/base.py
""" Abstract vector store interface

Stubbed, empty methods for testing
"""

from __future__ import annotations
from abc import ABC, abstractmethod

import numpy as np

from find_x.core.models import CodeChunk, SearchResult


class VectorStore(ABC):
    @abstractmethod
    def add(self, chunks: list[CodeChunk], embeddings: np.ndarray) -> None: ...

    @abstractmethod
    def search(self, query_embedding: np.ndarray, top_k: int) -> list[SearchResult]: ...


class EmptyVectorStore(VectorStore):
    def add(self, chunks: list[CodeChunk], embeddings: np.ndarray) -> None:
        pass

    def search(self, query_embedding: np.ndarray, top_k: int) -> list[SearchResult]:
        return []
    