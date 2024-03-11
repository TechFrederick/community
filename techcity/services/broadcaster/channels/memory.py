from techcity.models import Event
from techcity.services.broadcaster.channel import Channel


class MemoryChannel(Channel):
    """An in-memory channel that can be used for testing."""

    def __init__(self):
        self.events_sent = []

    def send(self, event: Event) -> bool:
        self.events_sent.append(event)
        return True
