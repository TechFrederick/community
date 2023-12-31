import json

import requests
from dotenv import load_dotenv

from .constants import cache
from .repositories import EventRepository, GroupRepository


def fetch(refresh=True):
    load_dotenv()
    event_repo = EventRepository()
    group_repo = GroupRepository()

    cache.mkdir(exist_ok=True)

    print("Fetching events...")
    if refresh:
        fetch_to_cache(group_repo)
    else:
        print("Using cached data...")

    generate_events(event_repo, group_repo)


def fetch_to_cache(group_repo):
    """Fetch the data from Meetup for each group and store it in the local cache."""
    session = requests.Session()

    for group in group_repo.all():
        response = session.get(
            f"https://api.meetup.com/{group.meetup_group_slug}/events"
        )
        response.raise_for_status()
        with open(cache / f"{group.slug}-events.json", "wb") as f:
            f.write(response.content)


def generate_events(event_repo: EventRepository, group_repo: GroupRepository) -> None:
    """Generate any events found in API data."""
    print("Scanning API response for events...")
    for group in group_repo.all():
        print(f"Parsing {group.name} events...")
        with open(cache / f"{group.slug}-events.json", "r") as f:
            event_data = json.load(f)

        for event in event_data:
            event_repo.create(group, event)
