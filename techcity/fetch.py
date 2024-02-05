import json

import requests
import typer
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from typing_extensions import Annotated
from urllib3.util import Retry

from .constants import cache
from .repositories import EventRepository, GroupRepository


def fetch(
    cached: Annotated[
        bool,
        typer.Option(help="Use cached response data instead of fetching from sources"),
    ] = False
) -> None:
    """Fetch data from API connections, normalize, and store in data directory."""
    load_dotenv()
    event_repo = EventRepository()
    group_repo = GroupRepository()

    cache.mkdir(exist_ok=True)

    print("Fetching events...")
    if cached:
        print("Using cached data...")
    else:
        fetch_to_cache(group_repo)

    generate_events(event_repo, group_repo)


def fetch_to_cache(group_repo):
    """Fetch the data from Meetup for each group and store it in the local cache."""
    retries = Retry(
        total=3,
        allowed_methods={"GET"},
        status_forcelist=[502, 503, 504],
        backoff_factor=0.1,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retries))

    for group in group_repo.all():
        response = session.get(
            f"https://api.meetup.com/{group.meetup_group_slug}/events",
            timeout=5,
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
