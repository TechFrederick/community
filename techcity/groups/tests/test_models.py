import pytest

from techcity.groups.models import Group
from techcity.groups.tests.factories import GroupFactory


class TestGroup:
    @pytest.mark.parametrize(
        "event_source, expected",
        (
            (Group.EventSource.WORDPRESS, True),
            (Group.EventSource.UNSPECIFIED, False),
        ),
    )
    def test_has_events(self, event_source, expected):
        """A group can report if it has any associated events."""
        assert GroupFactory(event_source=event_source).has_events == expected
