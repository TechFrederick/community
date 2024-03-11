from techcity.models import Event
from techcity.services.broadcaster.channel import Channel


class ConsoleChannel(Channel):
    """A console channel to broadcast on the terminal output."""

    def send(self, event: Event) -> bool:
        print(f"Broadcasting {event.id}")
        return True
