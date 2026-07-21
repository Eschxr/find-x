""" CLI entry point """

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from find_x.core.models import Query
from find_x.core.search import search_repo

app = typer.Typer()
console = Console()


@app.callback()
def callback() -> None:
    """ Find_X: LLM-independent semantic search over your codebase, because not every problem is best solved using AI. """


@app.command()
def search(
    repo_path: Path = typer.Argument(..., help="Path to the target repository"),
    query_text: str = typer.Argument(..., help="Search query"),
    top_k: int = typer.Option(5, "--top-k", "-k", help="Top-k results to return"),
    as_json: bool = typer.Option(False, "--json", help="Output as JSON instead of a table"),
) -> None:
    """ Search a repository using a natural language query """
    # Repo search entry point, orchestration delegated to src/find_x/core/search.py
    if not repo_path.is_dir():
        console.print(f"[red]Error:[/red] {repo_path} is not a directory")
        raise typer.Exit(code=1)

    results = search_repo(repo_path, Query(text=query_text, top_k=top_k))

    if as_json:
        print(json.dumps([r.model_dump() for r in results], indent=2))
        return
    
    if not results:
        console.print("[yellow]No results.[/yellow] (search pipeline is not implemented yet)")
        return

    table = Table(title=f"Results for: {query_text!r}")
    table.add_column("Score", justify="right")
    table.add_column("File")
    table.add_column("Lines")
    for r in results:
        table.add_row(f"{r.total_score:.3f}", r.chunk.repo_relative_path,
                    f"{r.chunk.start_line}-{r.chunk.end_line}")
        
    console.print(table)


if __name__ == "__main__":
    app()
    