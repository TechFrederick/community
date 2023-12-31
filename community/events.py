import os

import feedparser
import requests
from dotenv import load_dotenv

from .constants import cache
from .repositories import GroupRepository


def fetch(refresh=True):
    load_dotenv()
    group_repo = GroupRepository()

    cache.mkdir(exist_ok=True)

    print("Fetching events...")
    if refresh:
        fetch_to_cache(group_repo)
    else:
        print("Using cached data...")

    generate_events(group_repo)


def fetch_to_cache(group_repo):
    """Fetch the data from Meetup for each group and store it in the local cache."""
    session = requests.Session()
    login(session)

    for group in group_repo.all():
        # TODO: Remove once processing works generally.
        if group.slug != "python-frederick":
            print(f"Skipping {group.name}")
            continue

        cache_group_data(session, group, "rss")
        cache_group_data(session, group, "ical")


def login(session):
    """Do the login dance needed to get a valid authenticated session."""
    request_body = {
        "operationName": "login",
        "variables": {
            "input": {
                "email": os.environ["MEETUP_EMAIL"],
                "password": os.environ["MEETUP_PASSWORD"],
                "rememberMe": False,
            }
        },
        # Without this section, things break for reasons that I don't understand.
        # The Apollo docs seem to indicate that this is for persisting long query strings,
        # but the login request is done with a POST. *shrug*
        # I don't know how long Meetup will consider this a valid SHA.
        # I found this by inspecting the login payload.
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "27c2dcd3fe18741b545abf6918eb37aee203463028503aa8b2b959dc1c7aa007",
            }
        },
    }
    # This first request was required before login would work. It's probably setting
    # some initial cookies that must be present.
    response = session.get("https://www.meetup.com")
    response.raise_for_status()

    response = session.post("https://www.meetup.com/gql", json=request_body)
    data = response.json()
    if data["data"]["login"]["error"]:
        raise Exception("failed to login")


def cache_group_data(session, group, content_type):
    """Fetch the data and cache it.

    content_type must be `rss` or `ical` to get a valid URL from Meetup.
    """
    response = session.get(f"{group.url}events/{content_type}/")
    response.raise_for_status()
    with open(cache / f"{group.slug}.{content_type}", "wb") as f:
        f.write(response.content)


def generate_events(group_repo: GroupRepository) -> None:
    """Generate any events found in the Meetup RSS and iCal feeds."""
    print("Scanning RSS and iCal feeds for events...")
    events = {}
    for group in group_repo.all():
        # TODO: Remove once processing works generally.
        if group.slug != "python-frederick":
            continue

        group_events = {}
        events[group.slug] = group_events

        print(f"Parsing {group.name} feeds...")
        with open(cache / f"{group.slug}.rss", "r") as f:
            rss_data = feedparser.parse(f.read())

        for entry in rss_data["entries"]:
            group_events[entry["link"]] = {
                "title": entry["title"],
                "summary": entry["summary"],
            }

        # TODO: fill events from iCal file. Once the data is collected,
        # write to the `data` directory.
