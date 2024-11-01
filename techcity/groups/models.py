from __future__ import annotations

from django.db import models

from techcity.core.frontend import tailwindify_html


class GroupQuerySet(models.QuerySet):
    def by_source(self, event_source) -> GroupQuerySet:
        return self.filter(event_source=event_source).order_by("name")


GroupManager = models.Manager.from_queryset(GroupQuerySet)


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
    description = models.TextField()
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

    objects = GroupManager()

    def __str__(self):
        return self.name

    @property
    def card_image(self):
        return f"images/group-card/{self.slug}.png"

    @property
    def hero_image(self):
        return f"images/group-hero/{self.slug}.png"

    @property
    def html_description(self):
        # Wrap in a div because a root node is expected to format properly.
        return tailwindify_html(f"<div>{self.description}</div>")
