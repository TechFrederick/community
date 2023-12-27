import datetime
import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .repositories import GroupRepository

root = Path(__file__).parent.parent
public = root / "public"
environment = Environment(loader=FileSystemLoader(root / "templates"))


def main():
    start = datetime.datetime.now()
    print("Generating content to `out` directory")
    out = root / "out"
    out.mkdir(exist_ok=True)

    group_repo = GroupRepository()
    render_index(group_repo, out)
    render_groups(group_repo, out)

    copy_static(out)

    end = datetime.datetime.now()
    delta = end - start
    print(f"Done in {delta.total_seconds()} seconds")


def render_index(group_repo, out):
    print("Rendering index")
    render("index.html", {"groups": group_repo.all()}, out / "index.html")


def render_groups(group_repo: GroupRepository, out):
    groups_dir = out / "groups"
    groups_dir.mkdir(exist_ok=True)

    for group in group_repo.all():
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


def copy_static(out):
    print("Copying static files from `public` to `out`")
    for dirpath, _, filenames in os.walk(public):
        path = Path(dirpath)
        relpath = path.relative_to(public)
        outpath = out / relpath
        outpath.mkdir(exist_ok=True)

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            shutil.copyfile(filepath, outpath / filename)
