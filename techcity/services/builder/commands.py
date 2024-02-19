from techcity.events import BuildTriggered
from techcity.pubsub import publish


def build() -> None:
    """Build the web UI by rendering all available content."""
    publish(BuildTriggered())
