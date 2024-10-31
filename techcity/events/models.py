from __future__ import annotations

from datetime import datetime, timedelta

from django.db import models
from sqids.sqids import Sqids

from techcity.core.frontend import tailwindify_html

sqids = Sqids(
    min_length=8,
    alphabet="ymWpFqX0dzUK1jTM4RZ7sCukLf3bPrQ9ScVa6Y8wHNnhegiAoJ2OBlDvGI5xEt",
)


def combine_joint_events(events):
    """Combine any joint events as a single event.

    Any event that has the same time and venue as another event is assumed
    to be a joint event.
    """
    seen_events = {}
    combined_events = []
    for event in events:
        key = f"{event.start_at}-{event.venue_id}"
        if event.venue and key in seen_events:
            seen_events[key].is_joint = True
            continue
        seen_events[key] = event
        combined_events.append(event)
    return combined_events


class EventQuerySet(models.QuerySet):
    def filter_around(self, when: datetime) -> EventQuerySet:
        from_datetime = when - timedelta(days=30)
        to_datetime = when + timedelta(days=45)
        return self.filter_timeframe(from_datetime, to_datetime)

    def filter_timeframe(
        self,
        from_datetime: datetime | None = None,
        to_datetime: datetime | None = None,
    ) -> EventQuerySet:
        q = models.Q()
        if from_datetime:
            q = q & models.Q(start_at__gt=from_datetime)
        if to_datetime:
            q = q & models.Q(start_at__lt=to_datetime)
        return self.filter(q).order_by("start_at")

    def from_sqid(self, sqid: str) -> Event:
        decoded = sqids.decode(sqid)
        if not decoded:
            raise self.model.DoesNotExist()
        return self.get(id=decoded[0])


EventManager = models.Manager.from_queryset(EventQuerySet)


class Event(models.Model):
    """An event is the meeting of a group of people at a time and place."""

    name = models.CharField(max_length=256)
    url = models.URLField()
    # TODO: joint events need to be combined into a single event.
    # I don't think this should be modeled as a ManyToManyField
    # because each group may want their own description/info.
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    venue = models.ForeignKey(
        "events.Venue", blank=True, null=True, on_delete=models.SET_NULL
    )
    description = models.TextField()
    # TODO: There should be some kind of model that tracks Meetup IDs to events

    objects = EventManager()

    def __str__(self):
        return self.name

    @property
    def sqid(self):
        return sqids.encode([self.id])

    @property
    def is_all_day(self):
        """Anything longer than a work day is considered an all-day event"""
        return self.end_at - self.start_at > timedelta(hours=8)

    @property
    def html_description(self):
        # Wrap in a div because a root node is expected to format properly.
        return tailwindify_html(f"<div>{self.description}</div>")


class Venue(models.Model):
    """A physical place to hold an event."""

    address = models.CharField(max_length=256)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=32)
    zip = models.CharField(max_length=16)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}"


class EventRecordingType(models.TextChoices):
    YOUTUBE = "YOUTUBE", "YouTube"


class EventRecording(models.Model):
    """
    A recording of an event, such as a video or podcast.
    """

    # Related Models
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        help_text="The group that recorded the event",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        # Nullable, b/c there requires manual work to match the event
        # after the recording is ingested.
        null=True,
        blank=True,
        help_text="The event that was recorded",
    )

    # Recording Details
    recording_type = models.CharField(
        max_length=16,
        choices=EventRecordingType.choices,
        help_text="The type of recording",
    )
    title = models.CharField(
        max_length=256,
        help_text="The title of the recording",
    )
    description = models.TextField(
        help_text="A description of the recording",
    )
    # Including the URL here allows for more flexibility in the future,
    # such as linking to a podcast feed.
    # But for YouTube this is redundant with the external_id.
    url = models.URLField(
        help_text="The URL to the recording",
    )
    external_playlist_id = models.CharField(
        max_length=256,
        help_text="The ID of the playlist on the platform (i.e. list=<...> on YouTube)",
        null=True,
    )
    external_id = models.CharField(
        max_length=256,
        help_text="The ID of the recording on the platform (i.e. v=<...> on YouTube)",
        null=True,
    )
    metadata = models.JSONField(
        null=False,
        default=dict,
        help_text="Misc metadata about the recording",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_embed_url(self) -> str | None:
        if self.recording_type == EventRecordingType.YOUTUBE:
            return f"https://www.youtube.com/embed/{self.external_id}" + (
                f"?list={self.external_playlist_id}"
                if self.external_playlist_id
                else ""
            )
        return None

    def __str__(self):
        return self.title
