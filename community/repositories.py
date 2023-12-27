"""A reposiory handles loading and accessing model data"""


import yaml

from .constants import data_path
from .models import Group


class GroupRepository:
    def __init__(self):
        self._groups = self._load_groups()

    def _load_groups(self):
        groups = []
        groups_path = data_path / "groups"

        for filepath in sorted(groups_path.glob("*")):
            with open(filepath, "r") as f:
                documents = list(yaml.load_all(f, yaml.CLoader))
            frontmatter = documents[0]
            # TODO: transform description from Markdown into suitable HTML
            frontmatter["description"] = documents[1]
            groups.append(Group(**frontmatter))

        return groups

    def all(self):
        return self._groups
