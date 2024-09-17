from __future__ import annotations

from datetime import datetime, timedelta

from django.db import models
from sqids.sqids import Sqids

from techcity.core.frontend import tailwindify_html

sqids = Sqids(
    min_length=8,
    alphabet="ymWpFqX0dzUK1jTM4RZ7sCukLf3bPrQ9ScVa6Y8wHNnhegiAoJ2OBlDvGI5xEt",
)


class EventQuerySet(models.QuerySet):
    def filter_around(self, when: datetime) -> EventQuerySet:
        from_datetime = when - timedelta(days=30)
        to_datetime = when + timedelta(days=45)
        return self.filter(
            start_at__gt=from_datetime, start_at__lt=to_datetime
        ).order_by("start_at")

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
