class notification:
    """Represents a message or alert to be sent or logged."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"notification({self.message!r})"