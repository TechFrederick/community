from django.urls import reverse

from techcity.events.tests.factories import EventFactory


class TestIndex:
    def test_ok(self, client):
        EventFactory()

        response = client.get(reverse("core:index"))

        assert response.status_code == 200
