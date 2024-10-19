from django.urls import reverse

from techcity.events.tests.factories import EventFactory


class TestEventDetail:
    def test_ok(self, client):
        event = EventFactory()

        response = client.get(reverse("events:detail", args=[event.sqid]))

        assert response.status_code == 200

    def test_not_found(self, client):
        response = client.get(reverse("events:detail", args=["nope"]))

        assert response.status_code == 404


class TestEventsIcal:
    def test_ok(self, client):
        EventFactory()

        response = client.get(reverse("events:ical"))

        assert response.status_code == 200
