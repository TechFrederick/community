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


class Venue(BaseModel):
    """The location of an event"""

    address_1: str
    city: str
    state: str
    zip: str
    lat: float
    lon: float


class Event(BaseModel):
    """An event happening in town"""

    id: str
    group_slug: str
    name: str
    link: str
    description: str
    # Meetup provides the time in terms of Unix timestamps and a UTC offset
    time: int
    utc_offset: int
    venue: Venue
