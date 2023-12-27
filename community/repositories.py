"""A reposiory handles loading and accessing model data"""


from .models import Group


class GroupRepository:
    def __init__(self):
        self._groups = [
            Group(
                name="Amazon Web Services - Frederick",
                slug="aws-frederick",
                description="A Meetup group that discusses Amazon Web Services",
                teaser="AWS Frderick covers all things Amazon. The cloud is vast and so are Amazon's offerings. This group looks at all the cool tech that Amazon provides to build services for the web.",
            ),
            Group(
                name="Python Frederick",
                slug="python-frederick",
                description="A Meetup group that discusses the Python programming language",
                teaser="Python Frederick is a meetup group focused on building skills with the Python programming language. The group is the largest and most active Python group in the state of Maryland.",
            ),
        ]

    def all(self):
        return self._groups
