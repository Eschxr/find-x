# Find-X
Find "X" is a semantic explorer for GitHub repositories, allowing developers to query codebases using natural language instead of relying on exact keywords.

For example, a user could search:

- "Where is authentication handled?"
- "Find the database connection logic"
- "Show me code related to graph traversal"
- "Where are API routes defined?"
- "Find error handling around file uploads"

The project combines machine learning, information retrieval, code parsing, and practical software engineering. The plan is to begin as a local CLI tool and later expand into a web-based explorer or portfolio-integrated demo. 

## Goals

The primary goal is to build a semantic search layer over one or more GitHub repositories.

Must Have/Primary Requirements:

- Natural-language search over source code
- Code chunking by file, function, or class
- Embedding-based similarity search
- Useful result ranking and presentation
- A clean developer experience through a CLI or web UI

Should Have/Secondary Requirements:

- Supporting multiple repositories
- Showing syntax-highlighted snippets
- Linking results back to GitHub
- Comparing semantic search against keyword search
- Adding filters by language, repository, file type, or directory

## Core Features

The MVP should include:

- Repository ingestion from a local path
- File filtering by extension
- Code chunking into manageable units
- Embedding generation for each chunk
- Vector similarity search
- CLI query interface
- Ranked results with file path and code snippet

A more polished version could include:

- Web interface
- GitHub repository URL ingestion
- Syntax highlighting
- Search filters
- GitHub line-number links
- Hybrid search using both embeddings and keyword matching
- Result explanations, such as matched comments, function names, or nearby context

