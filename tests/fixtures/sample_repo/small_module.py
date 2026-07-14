"""Small module: 8 lines total, well under WINDOW_SIZE (40).

Exists to assert: a small file produces exactly one chunk spanning the
whole file, not zero and not a truncated window.
"""


def greet(name: str) -> str:
    return f"hello, {name}"
