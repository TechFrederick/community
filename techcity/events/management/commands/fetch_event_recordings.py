import os

from django.core.management.base import BaseCommand

from techcity.constants import cache
from techcity.events.connectors.youtube import YouTubeConnector


class Command(BaseCommand):
    help = "Fetch all event recordings from any of the source connectors"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cached",
            action="store_true",
            default=False,
            help="Use cached data instead of APIs if available",
        )
        parser.add_argument(
            "--youtube-api-key",
            type=str,
            help="The YouTube API key to use for fetching data"
            " (set in env YOUTUBE_API_KEY)",
            default=os.getenv("YOUTUBE_API_KEY"),
        )

    def handle(self, *args, cached: bool = False, youtube_api_key: str = "", **kwargs):
        self.stdout.write("Fetching events...")

        cache.mkdir(exist_ok=True)
        cache_dir = cache / "event_recordings"
        cache_dir.mkdir(exist_ok=True)

        connector = YouTubeConnector(
            cache_dir=cache_dir, youtube_api_key=youtube_api_key
        )
        connector.fetch(cached)
