from techcity.constants import cache
from techcity.services.groups.gateway import GroupsGateway

from .connectors.meetup import MeetupConnector
from .connectors.wordpress import WordPressConnector


def fetch(cached: bool, groups_gateway: GroupsGateway) -> None:
    """Fetch data from API connections, normalize, and store in data directory."""

    cache.mkdir(exist_ok=True)
    connectors = [
        MeetupConnector(),
        WordPressConnector(),
    ]

    print("Fetching events...")
    for connector in connectors:
        connector.fetch(groups_gateway.all(), cached)
