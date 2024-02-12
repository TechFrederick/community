"""A repository handles loading and accessing model data"""

import frontmatter
import markdown

from .constants import data_path
from .extensions import TailwindExtension


class HackathonRepository:
    def __init__(self):
        self.hackathons_path = data_path / "hackathons"
        self._hackathons = self._load_hackathons()

    def _load_hackathons(self):
        hackathons = []
        hackathons_path = data_path / "hackathons"

        for filepath in sorted(hackathons_path.glob("*")):
            with open(filepath, "r") as f:
                metadata, description = frontmatter.parse(f.read())
            description = markdown.markdown(
                description,
                extensions=[TailwindExtension()],
            )
            metadata["description"] = description
            hackathon = Hackathon(**metadata)  # type: ignore
            hackathons.append(hackathon)

        return hackathons

    def all(self):
        return self._hackathons
