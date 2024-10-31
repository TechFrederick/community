import json
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from techcity.events.models import EventRecording, EventRecordingType
from techcity.groups.models import Group

# TODO - this could be a model / added to Group. For now, hardcoding.
EVENT_RECORDING_SOURCES = {
    "python-frederick": "PLFcKEo4b_n1wMFhbiedpMgh2VRT5uICuF",
    "frederick-open-source": "PLFcKEo4b_n1zz3pGwC8e0RVaQf0c07jyd",
    "frederick-web-tech": "PLFcKEo4b_n1yistY9g3kyiXefYNPVZ1-X",
}


class YouTubeConnector:
    """A connector to fetch event recordings from YouTube.com"""

    def __init__(
        self,
        youtube_api_key: str,
        cache_dir: str,
        group_slugs: list[str] | None = None,
    ):
        self.youtube_api_key = youtube_api_key
        if not self.youtube_api_key:
            raise ValueError(
                "A YouTube API key is required to fetch data."
                "Set YOUTUBE_API_KEY in the environment."
            )

        self.cache_dir = cache_dir
        group_slugs = group_slugs or EVENT_RECORDING_SOURCES.keys()
        self.event_recording_sources = {
            group_slug: playlist_id
            for group_slug, playlist_id in EVENT_RECORDING_SOURCES.items()
            if group_slug in group_slugs
        }

    def fetch(self, cached: bool) -> None:
        print("Fetching event recordings from YouTube...")

        for group_slug, playlist_id in self.event_recording_sources.items():
            if cached:
                print(f"Using cached data for {group_slug}...")
            else:
                self.fetch_to_cache(group_slug, playlist_id)

            self.generate_event_recordings(group_slug, playlist_id)

    def fetch_to_cache(self, group_slug: str, playlist_id: str):
        """
        Fetch the data from YouTube and save it to the cache.

        Uses the following:
            https://developers.google.com/youtube/v3/docs/playlistItems/list
        """
        retries = Retry(
            total=3,
            allowed_methods={"GET"},
            status_forcelist=[502, 503, 504],
            backoff_factor=0.1,
        )
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=retries))

        results = []
        paginating = True
        page_token = ""

        while paginating:
            response = session.get(
                "https://www.googleapis.com/youtube/v3/playlistItems",
                params={
                    "part": ["id", "contentDetails", "snippet", "status"],
                    "playlistId": playlist_id,
                    "maxResults": 50,
                    "pageToken": page_token,
                    "key": self.youtube_api_key,
                },
                headers={
                    "Accept": "application/json",
                    "Referer": "https://techfrederick.org",
                },
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            results.extend(data["items"])
            if "nextPageToken" in data:
                page_token = data["nextPageToken"]
            else:
                paginating = False

        with open(self.cache_dir / f"{group_slug}-youtube-videos.json", "w") as f:
            json.dump(results, f)

    def generate_event_recordings(self, group_slug: str, playlist_id: str) -> None:
        """Generate any event recordings found in API data."""
        group = Group.objects.get(slug=group_slug)
        with open(self.cache_dir / f"{group_slug}-youtube-videos.json") as f:
            youtube_video_data = json.load(f)

        for video_data in youtube_video_data:
            self.upsert_event_recording(group, video_data, playlist_id)

    def upsert_event_recording(
        self,
        group: Group,
        youtube_video_data: dict,
        playlist_id: str,
    ) -> None:
        """Upsert an event recording into the database."""

        snippet = youtube_video_data["snippet"]
        content_details = youtube_video_data["contentDetails"]

        # TODO - could extract Speaker ? Should probably be from the
        #   _Meetup_ event ingestion, not YouTube.
        #
        # speaker_pattern = re.compile(r"(Speaker|Presenter): (.+)\n(.+)", re.DOTALL)
        # try:
        #     speaker_match = speaker_pattern.search(snippet["description"])
        #     speaker_name = speaker_match.group(2).strip()
        #     speaker_bio = speaker_match.group(3).strip()
        # except AttributeError:

        recording, created = EventRecording.objects.update_or_create(
            recording_type=EventRecordingType.YOUTUBE,
            group=group,
            external_id=content_details["videoId"],
            defaults={
                "title": snippet["title"],
                "description": snippet["description"],
                "url": f"https://www.youtube.com/watch?v={content_details['videoId']}&list={playlist_id}",
                "external_id": content_details["videoId"],
                "external_playlist_id": playlist_id,
                "metadata": {
                    "snippet": snippet,
                },
            },
        )

        if created:
            logging.info(f"Created new recording: {recording.title}")
        else:
            logging.info(f"Updated recording: {recording.title}")
