from django.urls import reverse

from techcity.events.tests.factories import EventFactory
from techcity.groups.tests.factories import GroupFactory


class TestGroupDetail:
    def test_ok(self, client):
        group = GroupFactory()

        response = client.get(reverse("groups:detail", args=[group.slug]))

        assert response.status_code == 200


class TestGroupEvents:
    def test_ok(self, client):
        event = EventFactory()

        response = client.get(reverse("groups:events", args=[event.group.slug]))

        assert response.status_code == 200
