import frontmatter
import markdown

from techcity.constants import data_path
from techcity.core.markdown_extensions import TailwindExtension
from techcity.models import Group


class GroupRepository:
    def __init__(self):
        self._groups_by_slug: dict[str, Group] = {}
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
            group = Group(**metadata)  # type: ignore
            groups.append(group)
            self._groups_by_slug[group.slug] = group

        return groups

    def all(self) -> list[Group]:
        return self._groups

    def find_by(self, slug: str) -> Group:
        """Find a group from its slug name.

        Invalid slugs are designed to fail so that bad data gets corrected.
        """
        return self._groups_by_slug[slug]
