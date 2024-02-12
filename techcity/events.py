from pydantic import BaseModel

from techcity.models import Group

# Commands


class FetchTriggered(BaseModel):
    """An event emitted when an operator requests a fetch"""

    cached: bool


# Integration Events


class EventPublished(BaseModel):
    """An event emitted when a physical event is published"""

    group: Group
    # FIXME: This raw data is a poor thing to pass around and will be refined
    # in a future change when a more normalized definition is created.
    event: dict
