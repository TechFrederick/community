from django.urls import reverse

from techcity.events.tests.factories import EventFactory


class TestEventDetail:
    def test_ok(self, client):
        event = EventFactory()

        response = client.get(reverse("events:detail", args=[event.sqid]))

        assert response.status_code == 200
