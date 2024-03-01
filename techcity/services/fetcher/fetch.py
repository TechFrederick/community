from techcity.constants import cache
from techcity.pubsub import PubSub
from techcity.services.groups.gateway import GroupsGateway

from .connectors.meetup import MeetupConnector
from .connectors.wordpress import WordPressConnector


def fetch(cached: bool, pubsub: PubSub, groups_gateway: GroupsGateway) -> None:
    """Fetch data from API connections, normalize, and store in data directory."""

    cache.mkdir(exist_ok=True)
    connectors = [
        MeetupConnector(pubsub),
        WordPressConnector(pubsub),
    ]

    print("Fetching events...")
    for connector in connectors:
        connector.fetch(groups_gateway.all(), cached)
