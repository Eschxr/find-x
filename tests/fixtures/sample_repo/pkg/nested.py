"""A module nested one directory deep."""


class Widget:
    """A trivial widget class, used as a stable target for future eval
    queries like 'where is the widget class defined'."""

    def __init__(self, label: str) -> None:
        self.label = label

    def render(self) -> str:
        return f"<widget label={self.label!r}>"
    