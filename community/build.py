from __future__ import annotations

import datetime
import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .constants import out, public, templates
from .repositories import EventRepository, GroupRepository
from .models import Event, Group

environment = Environment(loader=FileSystemLoader(templates))


def build():
    now = datetime.datetime.now()
    print("Generating content to `out` directory")
    out.mkdir(exist_ok=True)

    event_repo = EventRepository()
    group_repo = GroupRepository()
    render_index(now, event_repo, group_repo)
    render_groups(group_repo)

    copy_static()

    render_palette(group_repo)
    end = datetime.datetime.now()
    delta = end - now
    print(f"Done in {delta.total_seconds()} seconds")


def render_index(
    now: datetime.datetime,
    event_repo: EventRepository,
    group_repo: GroupRepository,
) -> None:
    print("Rendering index")

    events_with_group: list[tuple[Event, Group | None]] = []
    for event in event_repo.filter_around(now):
        if event.joint_with:
            events_with_group.append((event, None))
        else:
            events_with_group.append((event, group_repo.find_by(event.group_slug)))

    context = {
        "events_with_group": events_with_group,
        "groups": group_repo.all(),
    }
    render("index.html", context, out / "index.html")


def render_groups(group_repo: GroupRepository):
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


def copy_static():
    print("Copying static files from `public` to `out`")
    for dirpath, _, filenames in os.walk(public):
        path = Path(dirpath)
        relpath = path.relative_to(public)
        outpath = out / relpath
        outpath.mkdir(exist_ok=True)

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            shutil.copyfile(filepath, outpath / filename)


def render_palette(group_repo: GroupRepository) -> None:
    """Render the palette that Tailwind can pull from.

    This is a crud hack so that the Tailwind detection can find all the colors
    needed by different groups. Since all color usage is dynamic, there needs
    to be at least one output location that is controlled in the *source*
    that contains any color attributes that we want to use.
    """
    groups = group_repo.all()
    render("palette.html", {"groups": groups}, templates / "palette-rendered.html")
