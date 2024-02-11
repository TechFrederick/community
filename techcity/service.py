class Service:
    """A base service class which implements required interfaces"""

    consumes = []

    def dispatch(self, event) -> None:
        """Dispatch an event to an event handler."""
        raise NotImplementedError()
