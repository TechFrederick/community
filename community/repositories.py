"""A reposiory handles loading and accessing model data"""


import frontmatter
import markdown

from .constants import data_path
from .extensions import TailwindExtension
from .models import Group


class GroupRepository:
    def __init__(self):
        self._groups = self._load_groups()

    def _load_groups(self):
        groups = []
        groups_path = data_path / "groups"

        for filepath in sorted(groups_path.glob("*")):
            with open(filepath, "r") as f:
                metadata, description = frontmatter.parse(f.read())
            description = markdown.markdown(
                description,
                extensions=[TailwindExtension()],
            )
            metadata["description"] = description
            groups.append(Group(**metadata))

        return groups

    def all(self):
        return self._groups
