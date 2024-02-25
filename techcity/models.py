from __future__ import annotations

import enum
from datetime import datetime

from pydantic import BaseModel

from techcity.configuration import config


class MeetupGroupExtension(BaseModel):
    """Extension data for groups listed on Meetup"""

    # The group slug used on meetup.com
    slug: str


class GroupExtensions(BaseModel):
    """Extension data that may exist for a group"""

    meetup: MeetupGroupExtension | None = None


class Group(BaseModel):
    """A representation of a group that meets in town"""

    name: str
    slug: str
    url: str
    description: str
    teaser: str
    card_image: str
    hero_image: str
    # A brand color to associate with the group for accenting
    # The color should match an available color from Tailwind
    color: str
    extensions: GroupExtensions | None = None


class Venue(BaseModel):
    """The location of an event"""

    address: str
    city: str
    state: str
    zip: str
    lat: float
    lon: float

    def __eq__(self, other):
        """Are the venues the same?

        Since a community is almost exclusively for events locally,
        it should be sufficient (and fastest) to just compare the street address
        and city.
        """
        return (
            other
            and self.address.replace(".", "") == other.address.replace(".", "")
            and self.city == other.city
        )


class EventKind(str, enum.Enum):
    unspecified = "unspecified"
    hackathon = "hackathon"


class Event(BaseModel):
    """An event happening in town"""

    id: str
    kind: EventKind = EventKind.unspecified
    group_slug: str
    name: str
    link: str
    description: str
    start_at: datetime  # in UTC
    end_at: datetime  # in UTC
    venue: Venue | None = None
    joint_with: list[str] = []
    extensions: EventExtensions | None = None

    def __eq__(self, other):
        """When an event is at the same time and place, it is the same event."""
        return self.start_at == other.start_at and self.venue == other.venue

    def __hash__(self):
        """Generate a hash for this instance.

        Hashing is needed to make the set indices of the repository work.
        """
        return hash(self.id)

    @property
    def when(self) -> datetime:
        """Get the time in the localized form."""
        return self.start_at.astimezone(config.tz)

    @property
    def end(self):
        return self.end_at.astimezone(config.tz)


class EventExtensions(BaseModel):
    """Extension data that may exist for an event"""

    meetup: MeetupEventExtension | None = None


class MeetupEventExtension(BaseModel):
    """Extension data for an event originating from Meetup"""

    # The id used on meetup.com
    id: str


class EventListFilterOptions(BaseModel):
    """Options to use as filters when listing events"""

    from_datetime: datetime | None = None
    to_datetime: datetime | None = None
    group_slug: str | None = None


class Hackathon(BaseModel):
    """A hackathon event in town"""

    slug: str
    name: str
    color: str
    teaser: str
    description: str
