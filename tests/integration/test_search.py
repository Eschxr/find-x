"""Integration test for find_x.core.search.

Lives in tests/integration/, not tests/unit/, because it exercises the real
scanner + chunker + embedder together against the filesystem - unlike the
unit tests, a break here could mean any stage in the chain, not just one.
"""

import numpy as np

from find_x.core.models import Query, SearchResult
from find_x.core.search import search_repo
from find_x.storage.base import VectorStore


class FakeVectorStore(VectorStore):
    """Records what it was called with, returns a canned result - lets us
    assert search_repo wires the pipeline together correctly without
    depending on a real embedding model or index existing yet."""

    def __init__(self, canned_results=None):
        self.added_chunks = None
        self.added_embeddings = None
        self.canned_results = canned_results or []

    def add(self, chunks, embeddings):
        self.added_chunks = chunks
        self.added_embeddings = embeddings

    def search(self, query_embedding, top_k):
        return self.canned_results[:top_k]


def test_search_repo_returns_empty_list_with_default_store(sample_repo):
    results = search_repo(sample_repo, Query(text="anything"))
    assert results == []


def test_search_repo_populates_store_with_chunks_from_the_repo(sample_repo):
    store = FakeVectorStore()
    search_repo(sample_repo, Query(text="anything"), store=store)

    assert store.added_chunks is not None
    assert len(store.added_chunks) > 0
    assert store.added_embeddings.shape[0] == len(store.added_chunks)


def test_search_repo_returns_whatever_the_store_returns(sample_repo):
    # build a real chunk-backed result via the store itself instead of a dummy chunk
    store = FakeVectorStore()
    search_repo(sample_repo, Query(text="anything"), store=store)
    canned = [SearchResult(chunk=store.added_chunks[0], scores={"embedding": 0.9})]

    store2 = FakeVectorStore(canned_results=canned)
    results = search_repo(sample_repo, Query(text="anything", top_k=1), store=store2)

    assert results == canned


def test_search_repo_respects_top_k_via_the_store(sample_repo):
    store = FakeVectorStore()
    search_repo(sample_repo, Query(text="anything"), store=store)
    canned = [
        SearchResult(chunk=store.added_chunks[0], scores={"embedding": 0.9}),
        SearchResult(chunk=store.added_chunks[0], scores={"embedding": 0.5}),
    ]

    store2 = FakeVectorStore(canned_results=canned)
    results = search_repo(sample_repo, Query(text="anything", top_k=1), store=store2)

    assert len(results) == 1


def test_search_repo_resolves_unresolved_relative_paths(sample_repo, monkeypatch):
    from pathlib import Path

    monkeypatch.chdir(sample_repo)
    store = FakeVectorStore()
    # should not raise, even with an unresolved "." root
    search_repo(Path("."), Query(text="anything"), store=store)
    assert store.added_chunks is not None
