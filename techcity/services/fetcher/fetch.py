import json

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from techcity.constants import cache
from techcity.events import EventPublished
from techcity.pubsub import publish
from techcity.services.groups.gateway import GroupsGateway


def fetch(cached: bool, groups_gateway: GroupsGateway) -> None:
    """Fetch data from API connections, normalize, and store in data directory."""

    cache.mkdir(exist_ok=True)

    print("Fetching events...")
    if cached:
        print("Using cached data...")
    else:
        fetch_to_cache(groups_gateway)

    generate_events(groups_gateway)


def fetch_to_cache(groups_gateway: GroupsGateway):
    """Fetch the data from Meetup for each group and store it in the local cache."""
    retries = Retry(
        total=3,
        allowed_methods={"GET"},
        status_forcelist=[502, 503, 504],
        backoff_factor=0.1,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retries))

    for group in groups_gateway.all():
        response = session.get(
            f"https://api.meetup.com/{group.meetup_group_slug}/events",
            timeout=5,
        )
        response.raise_for_status()
        with open(cache / f"{group.slug}-events.json", "wb") as f:
            f.write(response.content)


def generate_events(groups_gateway: GroupsGateway) -> None:
    """Generate any events found in API data."""
    print("Scanning API response for events...")
    for group in groups_gateway.all():
        print(f"Parsing {group.name} events...")
        with open(cache / f"{group.slug}-events.json", "r") as f:
            event_data = json.load(f)

        for event in event_data:
            publish(EventPublished(group=group, event=event))
