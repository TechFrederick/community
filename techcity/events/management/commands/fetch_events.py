from django.core.management.base import BaseCommand

from techcity.constants import cache
from techcity.events.connectors.meetup import MeetupConnector


class Command(BaseCommand):
    help = "Fetch all events from any of the source connectors"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cached",
            action="store_true",
            default=False,
            help="Use cached data instead of APIs if available",
        )

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching events...")
        cached = kwargs["cached"]

        cache.mkdir(exist_ok=True)
        events_dir = cache / "events"
        events_dir.mkdir(exist_ok=True)

        connectors = [
            MeetupConnector(events_dir),
        ]

        for connector in connectors:
            connector.fetch(cached)
