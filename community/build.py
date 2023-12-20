from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel


class Group(BaseModel):
    """A representation of a group that meets in town"""

    name: str
    slug: str


def main():
    root = Path(__file__).parent.parent
    environment = Environment(loader=FileSystemLoader(root / "templates"))
    print("Generating content to `out` directory")
    out = root / "out"
    out.mkdir(exist_ok=True)

    render_groups(environment, out)
    print("Done")


def render_groups(environment, out):
    groups_dir = out / "groups"
    groups_dir.mkdir(exist_ok=True)

    groups = [
        Group(name="Python Frederick", slug="python-frederick"),
    ]
    for group in groups:
        render_group(environment, group, groups_dir)


def render_group(environment, group, groups_dir):
    print(f"Rendering group: {group.name}")
    group_dir = groups_dir / group.slug
    group_dir.mkdir(exist_ok=True)

    template = environment.get_template("group.html")
    with open(group_dir / "index.html", "w") as f:
        f.write(template.render(group=group))


if __name__ == "__main__":
    main()
