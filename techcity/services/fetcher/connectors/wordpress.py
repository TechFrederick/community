import datetime
import json

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from techcity.constants import cache
from techcity.core.ids import generate_id
from techcity.events import EventPublished
from techcity.models import Event, Group, Venue
from techcity.pubsub import PubSub


class WordPressConnector:
    """A connector to fetch data from a WordPress site"""

    def __init__(self, pubsub: PubSub) -> None:
        self.pubsub = pubsub

    def fetch(self, groups: list[Group], cached: bool) -> None:
        wordpress_groups = [
            group
            for group in groups
            if group.extensions is not None
            and group.extensions.wordpress is not None
            and group.extensions.wordpress.fetch_events
        ]
        if not wordpress_groups:
            return

        print("Fetching events from WordPress...")
        if cached:
            print("Using cached data...")
        else:
            self.fetch_to_cache(wordpress_groups)

        self.generate_events(wordpress_groups)

    def fetch_to_cache(self, groups: list[Group]) -> None:
        """Fetch the data from a WordPress site and store it in the local cache.

        This implementation is focused on pulling from The Events Calendar
        WordPress plugin.
        """
        for group in groups:
            self.fetch_group_to_cache(group)

    def fetch_group_to_cache(self, group: Group) -> None:
        events_endpoint = "wp-json/tribe/events/v1/events"
        if group.url.endswith("/"):
            url = f"{group.url}{events_endpoint}"
        else:
            url = f"{group.url}/{events_endpoint}"
        retries = Retry(
            total=3,
            allowed_methods={"GET"},
            status_forcelist=[502, 503, 504],
            backoff_factor=0.1,
        )
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=retries))
        # WordPress rejects the request unless it comes from something that looks
        # like a typical browser agent.
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) "
            "Gecko/20100101 Firefox/122.0"
        )

        response = session.get(url, timeout=5)
        response.raise_for_status()
        with open(cache / f"{group.slug}-wordpress-events.json", "wb") as f:
            f.write(response.content)

    def generate_events(self, groups: list[Group]):
        print("Scanning API response for events...")
        for group in groups:
            print(f"Parsing {group.name} events...")
            with open(cache / f"{group.slug}-wordpress-events.json") as f:
                event_data = json.load(f)

            events = event_data["events"]
            for event in events:
                venue = None
                if event["venue"].get("address"):
                    venue = Venue(
                        address=event["venue"]["address"],
                        city=event["venue"]["city"],
                        state=event["venue"]["province"],
                        zip=event["venue"]["zip"],
                    )

                start_at = datetime.datetime.strptime(
                    event["utc_start_date"], "%Y-%m-%d %H:%M:%S"
                )
                start_at = start_at.replace(tzinfo=datetime.UTC)
                end_at = datetime.datetime.strptime(
                    event["utc_end_date"], "%Y-%m-%d %H:%M:%S"
                )
                end_at = end_at.replace(tzinfo=datetime.UTC)
                event_model = Event(
                    id=generate_id(str(event["id"]), "wordpress"),
                    group_slug=group.slug,
                    name=event["title"],
                    link=event["url"],
                    description=event["description"],
                    start_at=start_at,
                    end_at=end_at,
                    venue=venue,
                )
                self.pubsub.publish(EventPublished(event=event_model))
