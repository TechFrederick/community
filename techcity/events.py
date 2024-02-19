from pydantic import BaseModel

from techcity.models import Event

# Commands


class BuildTriggered(BaseModel):
    """An event emitted when an operator requests a build"""


class FetchTriggered(BaseModel):
    """An event emitted when an operator requests a fetch"""

    cached: bool


# Integration Events


class EventPublished(BaseModel):
    """An event emitted when a physical event is published"""

    event: Event
