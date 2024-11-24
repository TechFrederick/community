from django.urls import reverse

from techcity.events.tests.factories import EventFactory


class TestIndex:
    def test_ok(self, client):
        EventFactory()

        response = client.get(reverse("core:index"))

        assert response.status_code == 200


class TestManifest:
    def test_ok(self, client):
        response = client.get(reverse("core:manifest"))

        assert response.status_code == 200


class TestUp:
    def test_ok(self, client):
        response = client.get(reverse("core:up"))

        assert response.status_code == 200


class TestGetBrand:
    def test_ok(self, client):
        response = client.get(reverse("api:brand"))

        assert response.status_code == 200
