class Service:
    """A base service class which implements required interfaces"""

    # A service can list the events that it consumes.
    # These events will be subscribed to in the pubsub system.
    consumes = []

    def dispatch(self, event) -> None:
        """Dispatch an event to an event handler."""
        if self.consumes:
            raise NotImplementedError()
