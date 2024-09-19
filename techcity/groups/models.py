from django.db import models

from techcity.core.frontend import tailwindify_html


class Group(models.Model):
    """A group represents any collection of people.

    This could be a Meetup group, a company, a non-profit, etc.
    """

    name = models.CharField(max_length=128)
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
