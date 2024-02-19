from __future__ import annotations

import datetime
import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from techcity.constants import out, public, templates
from techcity.core.frontend import tailwindify_html
from techcity.models import Event, Group
from techcity.repositories import HackathonRepository
from techcity.services.events.repository import EventRepository
from techcity.services.groups.repository import GroupRepository

environment = Environment(loader=FileSystemLoader(templates), autoescape=True)
# If this code is still in operation in 50 years, that would be shocking.
# We need a time delta that can stand in for the distant past to pull all events.
old_delta = datetime.timedelta(days=50 * 365)


def build() -> None:
    """Build the web UI by rendering all available content."""
    now = datetime.datetime.now(tz=datetime.UTC)
    print("Generating content to `out` directory")
    out.mkdir(exist_ok=True)

    # FIMXE: This should be replaced by the gateway in a future change.
    event_repo = EventRepository()
    # FIMXE: This should be replaced by the gateway in a future change.
    group_repo = GroupRepository()
    hackathon_repo = HackathonRepository()
    render_index(now, event_repo, group_repo, hackathon_repo)
    render_events(event_repo, group_repo)
    render_groups(now, group_repo, event_repo)
    render_hackathons(hackathon_repo)

    copy_static()

    render_palette(group_repo, hackathon_repo)
    end = datetime.datetime.now(tz=datetime.UTC)
    delta = end - now
    print(f"Done in {delta.total_seconds()} seconds")


def render_index(
    now: datetime.datetime,
    event_repo: EventRepository,
    group_repo: GroupRepository,
    hackathon_repo: HackathonRepository,
) -> None:
    print("Rendering index")

    upcoming_events_with_group: list[tuple[Event, Group | None]] = []
    recent_events_with_group: list[tuple[Event, Group | None]] = []
    events_with_group = upcoming_events_with_group
    for event in event_repo.filter_around(now):
        if event.when < now:
            events_with_group = recent_events_with_group
        if event.joint_with:
            events_with_group.append((event, None))
        else:
            events_with_group.append((event, group_repo.find_by(event.group_slug)))

    context = {
        "upcoming_events_with_group": reversed(upcoming_events_with_group),
        "recent_events_with_group": recent_events_with_group,
        "groups": group_repo.all(),
        "hackathons": hackathon_repo.all(),
        "now": now,
    }
    render("index.html", context, out / "index.html")


def render_events(
    event_repo: EventRepository,
    group_repo: GroupRepository,
) -> None:
    print("Rendering events")
    events_dir = out / "events"
    events_dir.mkdir(exist_ok=True)

    for event in event_repo.all():
        event_dir = events_dir / event.id
        event_dir.mkdir(exist_ok=True)
        context = {
            # Wrap in a div because a root node is expected to format properly.
            "description": tailwindify_html(f"<div>{event.description}</div>"),
            "event": event,
            "group": group_repo.find_by(event.group_slug),
        }
        render("event.html", context, event_dir / "index.html")


def render_groups(
    now: datetime.datetime,
    group_repo: GroupRepository,
    event_repo: EventRepository,
):
    groups_dir = out / "groups"
    groups_dir.mkdir(exist_ok=True)

    for group in group_repo.all():
        events = event_repo.filter_group(group.slug, now)
        render_group(now, group, events, groups_dir)
        all_events = event_repo.filter_group(group.slug, now, past=old_delta)
        render_group_events(group, all_events, groups_dir)


def render_group(now, group, events, groups_dir):
    print(f"Rendering group: {group.name}")
    group_dir = groups_dir / group.slug
    group_dir.mkdir(exist_ok=True)

    context = {
        "events": events,
        "group": group,
        "now": now,
    }
    render("group.html", context, group_dir / "index.html")


def render_group_events(group, events, groups_dir):
    print(f"Rendering group events: {group.name}")
    events_dir = groups_dir / group.slug / "events"
    events_dir.mkdir(exist_ok=True)

    context = {
        "events": events,
        "group": group,
    }
    render("group_events.html", context, events_dir / "index.html")


def render_hackathons(hackathon_repo: HackathonRepository):
    hackathons_dir = out / "hackathons"
    hackathons_dir.mkdir(exist_ok=True)

    for hackathon in hackathon_repo.all():
        render_hackathon(hackathon, hackathons_dir)


def render_hackathon(hackathon, hackathons_dir):
    print(f"Rendering hackathon: {hackathon.name}")
    hackathon_dir = hackathons_dir / hackathon.slug
    hackathon_dir.mkdir(exist_ok=True)

    context = {
        "hackathon": hackathon,
    }
    render("hackathon.html", context, hackathon_dir / "index.html")


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


def render_palette(
    group_repo: GroupRepository, hackathon_repo: HackathonRepository
) -> None:
    """Render the palette that Tailwind can pull from.

    This is a crud hack so that the Tailwind detection can find all the colors
    needed by different groups. Since all color usage is dynamic, there needs
    to be at least one output location that is controlled in the *source*
    that contains any color attributes that we want to use.
    """
    render(
        "palette.html",
        {
            "groups": group_repo.all(),
            "hackathons": hackathon_repo.all(),
        },
        templates / "palette-rendered.html",
    )
