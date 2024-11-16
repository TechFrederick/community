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


class BoundingBox:
    """A bounding box for OpenStreetMap embedding"""

    # A constant offset to define a reasonable looking bounding box.
    offset = 0.0012

    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    @property
    def top_left(self):
        lat = float(self.lat) + self.offset
        long = float(self.long) - self.offset
        return f"{long}%2C{lat}"

    @property
    def bottom_right(self):
        lat = float(self.lat) - self.offset
        long = float(self.long) + self.offset
        return f"{long}%2C{lat}"


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

    @property
    def has_map(self):
        return self.venue and self.venue.lat and self.venue.long

    @property
    def bbox(self):
        return BoundingBox(self.venue.lat, self.venue.long)


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
