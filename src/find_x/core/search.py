#src/find_x/core/search.py
""" The main orchestrator, pipeline logic here only, don't seep logic into cli.py (& web API later) """

from __future__ import annotations
from pathlib import Path

from find_x.core import chunker, embedder, scanner
from find_x.core.models import Query, SearchResult
from find_x.storage.base import EmptyVectorStore, VectorStore


def search_repo(
    repo_root: Path,
    query: Query,
    store: VectorStore | None = None,
) -> list[SearchResult]:
    """ Run the full pipeline against a repo & return ranked results """
    store = store or EmptyVectorStore()

    repo_root = repo_root.resolve()

    files = scanner.scan_repo(repo_root)
    chunks = chunker.chunk_repo(files, repo_root)
    embeddings = embedder.embed_chunks(chunks)
    store.add(chunks, embeddings)

    query_embedding = embedder.embed_query(query.text)
    return store.search(query_embedding, top_k=query.top_k)
