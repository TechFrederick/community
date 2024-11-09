import datetime
import json

import requests
import stamina

from techcity.events.models import Event, Venue
from techcity.groups.models import Group


class MeetupConnector:
    """A connector to fetch data from Meetup.com"""

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def fetch(self, cached: bool) -> None:
        print("Fetching events from Meetup...")
        groups = Group.objects.by_source(Group.EventSource.MEETUP)

        if cached:
            print("Using cached data...")
        else:
            self.fetch_to_cache(groups)

        self.generate_events(groups)

    def fetch_to_cache(self, groups: list[Group]):
        """Fetch the data from Meetup for each group and store it in the local cache."""
        for group in groups:
            response = self.fetch_events(group)
            with open(self.cache_dir / f"{group.slug}.json", "wb") as f:
                f.write(response.content)

    @stamina.retry(on=requests.RequestException)
    def fetch_events(self, group):
        response = requests.get(
            f"https://api.meetup.com/{group.event_source_id}/events",
            timeout=5,
        )
        response.raise_for_status()
        return response

    def generate_events(self, groups: list[Group]) -> None:
        """Generate any events found in API data."""
        print("Scanning API response for events...")
        for group in groups:
            print(f"Parsing {group.name} events...")
            with open(self.cache_dir / f"{group.slug}.json") as f:
                event_data = json.load(f)

            for event in event_data:
                # Meetup provides the time in terms of Unix timestamps and a UTC offset
                # The times are provided in ms instead of seconds.
                start_at = datetime.datetime.fromtimestamp(
                    event["time"] / 1000, tz=datetime.UTC
                )
                end_at = start_at + datetime.timedelta(milliseconds=event["duration"])

                defaults = {
                    "name": event["name"],
                    "group": group,
                    "start_at": start_at,
                    "end_at": end_at,
                    "description": event["description"],
                }

                if event["venue"]:
                    venue_defaults = {
                        "state": event["venue"].get("state", ""),
                        "zip": event["venue"].get("zip", ""),
                        "lat": event["venue"]["lat"],
                        "long": event["venue"]["lon"],
                    }
                    venue, _ = Venue.objects.update_or_create(
                        address=event["venue"]["address_1"].strip().rstrip(","),
                        city=event["venue"]["city"].strip(),
                        defaults=venue_defaults,
                    )
                    defaults["venue"] = venue

                Event.objects.update_or_create(url=event["link"], defaults=defaults)
