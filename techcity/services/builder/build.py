from __future__ import annotations

import datetime
import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from techcity.constants import data_path, out
from techcity.core.frontend import tailwindify_html
from techcity.models import Event, Group, Hackathon
from techcity.repositories import HackathonRepository
from techcity.services.events.gateway import EventsGateway
from techcity.services.groups.gateway import GroupsGateway

# If this code is still in operation in 50 years, that would be shocking.
# We need a time delta that can stand in for the distant past to pull all events.
old_delta = datetime.timedelta(days=50 * 365)


def build(events_gateway: EventsGateway, groups_gateway: GroupsGateway) -> None:
    """Build the web UI by rendering all available content."""
    now = datetime.datetime.now(tz=datetime.UTC)
    builder = SiteBuilder(events_gateway, groups_gateway, now, out)
    builder.build()


class SiteBuilder:
    """Site builder builds the site output."""

    def __init__(
        self,
        events_gateway: EventsGateway,
        groups_gateway: GroupsGateway,
        now: datetime.datetime,
        out: Path,
    ):
        self.events_gateway = events_gateway
        self.groups_gateway = groups_gateway
        self.now = now
        self.out = out
        service_path = Path(__file__).parent
        self.templates = service_path / "templates"
        self.public = service_path / "public"
        self.environment = Environment(
            loader=FileSystemLoader(self.templates), autoescape=True
        )

    def build(self):
        print("Generating content to `out` directory")
        self.out.mkdir(exist_ok=True)

        # FIXME: This should be replaced by the gateway in a future change.
        hackathon_repo = HackathonRepository()

        self.render_index(hackathon_repo)
        self.render_events()
        self.render_groups()
        self.render_hackathons(hackathon_repo)
        self.render_palette(hackathon_repo)

        self.copy_static()

        end = datetime.datetime.now(tz=datetime.UTC)
        delta = end - self.now
        print(f"Done in {delta.total_seconds()} seconds")

    def render(self, template_name, context, out_path):
        template = self.environment.get_template(template_name)
        with open(out_path, "w") as f:
            f.write(template.render(**context))

    def copy_static(self):
        print("Copying static files from `public` to `out`")
        self.copy_dir(self.public)
        data_public = data_path / "public"
        if data_public.exists():
            self.copy_dir(data_public)

    def copy_dir(self, direcectory):
        for dirpath, _, filenames in os.walk(direcectory):
            path = Path(dirpath)
            relpath = path.relative_to(direcectory)
            outpath = self.out / relpath
            outpath.mkdir(exist_ok=True)

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                shutil.copyfile(filepath, outpath / filename)

    def render_index(
        self,
        hackathon_repo: HackathonRepository,
    ) -> None:
        print("Rendering index")

        upcoming_events_with_group: list[tuple[Event, Group | None]] = []
        recent_events_with_group: list[tuple[Event, Group | None]] = []
        events_with_group = upcoming_events_with_group
        for event in self.events_gateway.filter_around(self.now):
            if event.when < self.now:
                events_with_group = recent_events_with_group
            if event.joint_with:
                events_with_group.append((event, None))
            else:
                group = self.groups_gateway.retrieve(event.group_slug)
                events_with_group.append((event, group))

        context = {
            "upcoming_events_with_group": reversed(upcoming_events_with_group),
            "recent_events_with_group": recent_events_with_group,
            "groups": self.groups_gateway.all(),
            "hackathons": hackathon_repo.all(),
            "now": self.now,
        }
        self.render("index.html", context, self.out / "index.html")

    def render_events(
        self,
    ) -> None:
        print("Rendering events")
        events_dir = self.out / "events"
        events_dir.mkdir(exist_ok=True)

        for event in self.events_gateway.all():
            event_dir = events_dir / event.id
            event_dir.mkdir(exist_ok=True)
            context = {
                # Wrap in a div because a root node is expected to format properly.
                "description": tailwindify_html(f"<div>{event.html_description}</div>"),
                "event": event,
                "group": self.groups_gateway.retrieve(event.group_slug),
            }
            self.render("event.html", context, event_dir / "index.html")

    def render_groups(self):
        groups_dir = self.out / "groups"
        groups_dir.mkdir(exist_ok=True)

        old_dt = self.now - old_delta
        from_dt = self.now - datetime.timedelta(days=30)
        to_dt = self.now + datetime.timedelta(days=45)
        for group in self.groups_gateway.all():
            slug = group.slug
            events = self.events_gateway.filter_group(slug, from_dt, to_dt)
            self.render_group(group, events, groups_dir)
            all_events = self.events_gateway.filter_group(slug, old_dt, to_dt)
            self.render_group_events(group, all_events, groups_dir)

    def render_group(
        self,
        group: Group,
        events: list[Event],
        groups_dir: Path,
    ) -> None:
        print(f"Rendering group: {group.name}")
        group_dir = groups_dir / group.slug
        group_dir.mkdir(exist_ok=True)

        context = {
            "events": events,
            "group": group,
            "now": self.now,
        }
        self.render("group.html", context, group_dir / "index.html")

    def render_group_events(
        self,
        group: Group,
        events: list[Event],
        groups_dir: Path,
    ) -> None:
        print(f"Rendering group events: {group.name}")
        events_dir = groups_dir / group.slug / "events"
        events_dir.mkdir(exist_ok=True)

        context = {
            "events": events,
            "group": group,
        }
        self.render("group_events.html", context, events_dir / "index.html")

    def render_hackathons(self, hackathon_repo: HackathonRepository):
        hackathons_dir = self.out / "hackathons"
        hackathons_dir.mkdir(exist_ok=True)

        for hackathon in hackathon_repo.all():
            self.render_hackathon(hackathon, hackathons_dir)

    def render_hackathon(
        self,
        hackathon: Hackathon,
        hackathons_dir: Path,
    ) -> None:
        print(f"Rendering hackathon: {hackathon.name}")
        hackathon_dir = hackathons_dir / hackathon.slug
        hackathon_dir.mkdir(exist_ok=True)

        context = {
            "hackathon": hackathon,
        }
        self.render("hackathon.html", context, hackathon_dir / "index.html")

    def render_palette(
        self,
        hackathon_repo: HackathonRepository,
    ) -> None:
        """Render the palette that Tailwind can pull from.

        This is a crud hack so that the Tailwind detection can find all the colors
        needed by different groups. Since all color usage is dynamic, there needs
        to be at least one output location that is controlled in the *source*
        that contains any color attributes that we want to use.
        """
        self.render(
            "palette.html",
            {
                "groups": self.groups_gateway.all(),
                "hackathons": hackathon_repo.all(),
            },
            self.templates / "palette-rendered.html",
        )
