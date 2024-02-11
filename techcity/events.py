from pydantic import BaseModel

# Commands


class FetchTriggered(BaseModel):
    """An event emitted when an operator requests a fetch"""

    cached: bool
