# src/find_x/core/models.py
""" Core data models, shared across chunking, embedding, storage & search """

from __future__ import annotations

import hashlib
from typing import Any, Literal

from pydantic import BaseModel, Field, computed_field

# Definition for chunk types kept as literal not enum so
# changes don't break everywhere this is used
ChunkType = Literal["line_range", "function", "class", "module"]


class CodeChunk(BaseModel):
    """ A unit of code to be embedded and searched over """
    id: str
    repo_relative_path: str
    language: str
    chunk_type: ChunkType
    start_line: int
    end_line: int
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)

    @computed_field
    @property
    def line_count(self) -> int:
        return self.end_line - self.start_line + 1

    @staticmethod
    def compute_id(repo_relative_path: str, start_line: int, end_line: int) -> str:
        """ sha256 hash ID """
        raw = f"{repo_relative_path}:{start_line}-{end_line}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    
    def model_post_init(self, __context: Any) -> None:
        if self.start_line > self.end_line:
            raise ValueError(
                f"start_line ({self.start_line}) > end_line ({self.end_line}) "
                f"in {self.repo_relative_path}"
            )
        

class SearchResult(BaseModel):
    """ Singular ranked result returned from an arbitrary query """
    chunk: CodeChunk
    scores: dict[str, float] = Field(default_factory=dict)

    @computed_field
    @property
    def total_score(self) -> float:
        return sum(self.scores.values())


class Query(BaseModel):
    """ An arbitrary search query """
    text: str
    top_k: int = 5
    