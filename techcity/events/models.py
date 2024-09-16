from __future__ import annotations

from datetime import datetime, timedelta

from django.db import models


class EventQuerySet(models.QuerySet):
    def filter_around(self, when: datetime) -> EventQuerySet:
        from_datetime = when - timedelta(days=30)
        to_datetime = when + timedelta(days=45)
        return self.filter(
            start_at__gt=from_datetime, start_at__lt=to_datetime
        ).order_by("start_at")


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


class Venue(models.Model):
    """A physical place to hold an event."""

    address = models.CharField(max_length=256)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=32)
    zip = models.CharField(max_length=16)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
