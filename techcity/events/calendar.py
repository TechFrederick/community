from collections.abc import Iterable

from icalendar import Calendar
from icalendar import Event as CalendarEvent

from .models import Event


def make_calendar(calendar_name: str, events: Iterable[Event]) -> Calendar:
    """Make an iCalendar containing the provided events."""
    calendar = Calendar()
    calendar.add("prodid", "-//techfrederick Community//Community Website//EN")
    calendar.add("version", "2.0")
    calendar.add("x-wr-calname", calendar_name)

    for event in events:
        calendar_event = CalendarEvent()
        calendar_event.add("summary", event.name)
        calendar_event.add("uid", event.id)
        calendar_event.add("description", event.description)
        # FIXME: We don't currently track a created or last modified datetime
        # on an event, but dtstamp is required. Use the start time has a stand-in.
        # The impact of this is that calendar clients won't really update an event
        # unless the start time changes, which isn't great.
        calendar_event.add("dtstamp", event.start_at)
        calendar_event.start = event.start_at
        calendar_event.end = event.end_at
        calendar.add_component(calendar_event)

    return calendar
