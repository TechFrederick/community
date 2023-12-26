from pydantic import BaseModel


class Group(BaseModel):
    """A representation of a group that meets in town"""

    name: str
    slug: str
    description: str
