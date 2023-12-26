"""A reposiory handles loading and accessing model data"""


from .models import Group


class GroupRepository:
    def __init__(self):
        self._groups = [
            Group(
                name="Python Frederick",
                slug="python-frederick",
                description="A Meetup group that discusses the Python programming language",
            ),
        ]

    def all(self):
        return self._groups
