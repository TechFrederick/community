import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .models import Group

root = Path(__file__).parent.parent
environment = Environment(loader=FileSystemLoader(root / "templates"))


def main():
    start = datetime.datetime.now()
    print("Generating content to `out` directory")
    out = root / "out"
    out.mkdir(exist_ok=True)

    render_index(out)
    render_groups(out)
    end = datetime.datetime.now()
    delta = end - start
    print(f"Done in {delta.total_seconds()} seconds")


def render_index(out):
    print("Rendering index")
    render("index.html", {}, out / "index.html")


def render_groups(out):
    groups_dir = out / "groups"
    groups_dir.mkdir(exist_ok=True)

    groups = [
        Group(
            name="Python Frederick",
            slug="python-frederick",
            description="A Meetup group that discusses the Python programming language",
        ),
    ]

    print("Rendering groups index")
    render("groups.html", {"groups": groups}, groups_dir / "index.html")

    for group in groups:
        render_group(group, groups_dir)


def render_group(group, groups_dir):
    print(f"Rendering group: {group.name}")
    group_dir = groups_dir / group.slug
    group_dir.mkdir(exist_ok=True)

    render("group.html", {"group": group}, group_dir / "index.html")


def render(template_name, context, out_path):
    template = environment.get_template(template_name)
    with open(out_path, "w") as f:
        f.write(template.render(**context))
