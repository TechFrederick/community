from __future__ import annotations

from pathlib import Path

from django.db import models
from django_prose_editor.fields import ProseEditorField

from techcity.core.frontend import tailwindify_html


class GroupQuerySet(models.QuerySet):
    def by_source(self, event_source) -> GroupQuerySet:
        return self.filter(event_source=event_source).order_by("name")


GroupManager = models.Manager.from_queryset(GroupQuerySet)


def card_image_path(instance, filename):
    path = Path(filename)
    return f"groups/card-image/{instance.slug}{path.suffix}"


def hero_image_path(instance, filename):
    path = Path(filename)
    return f"groups/hero-image/{instance.slug}{path.suffix}"


class Group(models.Model):
    """A group represents any collection of people.

    This could be a Meetup group, a company, a non-profit, etc.
    """

    class EventSource(models.TextChoices):
        UNSPECIFIED = "unspecified"
        MEETUP = "meetup"
        WORDPRESS = "wordpress"

    class Kind(models.TextChoices):
        UNKNOWN = "unknown", "Unknown"
        COMMUNITY = "community", "Community"
        NONPROFIT = "nonprofit", "Nonprofit"
        COMPANY = "company", "Company"

    name = models.CharField(max_length=128)
    kind = models.CharField(
        max_length=16,
        default=Kind.UNKNOWN,
        choices=Kind.choices,
        db_index=True,
        help_text="The broad category of a group",
    )
    slug = models.SlugField()
    url = models.URLField(max_length=256)
    description = ProseEditorField()
    teaser = models.TextField()
    color = models.CharField(
        max_length=32,
        help_text=(
            "A theme color to use for display purposes. "
            "Must be a Tailwind color like `blue-500`."
        ),
    )
    event_source = models.CharField(
        max_length=16,
        default=EventSource.UNSPECIFIED,
        choices=EventSource.choices,
        help_text="What is the source of event information for this group",
    )
    event_source_id = models.CharField(
        max_length=32,
        blank=True,
        help_text="An optional ID to use when checking an event source",
    )
    card_image = models.FileField(
        upload_to=card_image_path,
        help_text="The small image format used when displaying a card",
    )
    hero_image = models.FileField(
        upload_to=hero_image_path,
        help_text="The large image format used when displaying the group detail page",
    )

    objects = GroupManager()

    def __str__(self):
        return self.name

    @property
    def hero_image_static(self):
        """TODO: remove this. Using `_static` to deconflict with the field name."""
        return f"images/group-hero/{self.slug}.png"

    @property
    def html_description(self):
        # Wrap in a div because a root node is expected to format properly.
        return tailwindify_html(f"<div>{self.description}</div>")

    @property
    def has_events(self) -> bool:
        """Does the group have any events?

        Rather than querying the events table, assume that a group with
        no event source has no events.
        """
        return self.event_source != self.EventSource.UNSPECIFIED
