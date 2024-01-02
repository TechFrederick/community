from datetime import datetime, timedelta, timezone

from pydantic import BaseModel


class Group(BaseModel):
    """A representation of a group that meets in town"""

    name: str
    slug: str
    # Meetup has different slugs from what the community site uses.
    meetup_group_slug: str
    url: str
    description: str
    teaser: str
    card_image: str
    hero_image: str
    # A brand color to associate with the group for accenting
    # The color should match an available color from Tailwind
    color: str


class Venue(BaseModel):
    """The location of an event"""

    address_1: str
    city: str
    state: str
    zip: str
    lat: float
    lon: float

    def __eq__(self, other):
        """Are the venues the same?

        Since this community is almost exclusively for events in the county,
        it should be sufficient (and fastest) to just compare the street address.

        Meetup is a dump and includes multiple addresses for the same place,
        differentiated by only punctuation. This will try to normalize
        by removing the punctuation.
        """
        return self.address_1.replace(".", "") == other.address_1.replace(".", "")


class Event(BaseModel):
    """An event happening in town"""

    id: str
    group_slug: str
    name: str
    link: str
    description: str
    # Meetup provides the time in terms of Unix timestamps and a UTC offset
    # The times are provided in ms instead of seconds.
    time: int
    utc_offset: int
    duration: int
    venue: Venue
    joint_with: list[str] = []

    def __eq__(self, other):
        """When an event is at the same time and place, it is the same event."""
        return self.time == other.time and self.venue == other.venue

    def __hash__(self):
        """Generate a hash for this instance.

        Hashing is needed to make the set indices of the repository work.
        """
        return hash(self.id)

    @property
    def when(self):
        """Get the time in the form of a more flexible datetime for formatting."""
        tz = timezone(timedelta(milliseconds=self.utc_offset))
        dt = datetime.fromtimestamp(self.time / 1000, tz=tz)
        return dt
