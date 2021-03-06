import pytest

from django.urls import reverse

from typing import Dict

from rest_framework import status
from rest_framework.test import APIClient

from agile.models import Agile
from agile.tests.factory.agile_factory import AgileFactory
from agile.tests.factory.user_factory import UserFactory
from .utils import validate_uuid4


@pytest.fixture
def logged_in_client() -> APIClient:
    """Setup a fixture for an APIClient with a logged in user."""
    user = UserFactory()
    user.set_password("password")
    user.save()
    client = APIClient()
    client.login(username=user.username, password="password")
    return client


@pytest.mark.django_db
class TestAgileViews:
    @pytest.fixture
    def defaults(self) -> Dict[str, Dict[str, str]]:
        payload = {
            "name": "Working product over comprehensive documentation",
            "description": "The Agile values dictate that the first and foremost duty",
        }
        return {
            "payload": payload,
        }

    def get_detail_url(self, value_id):
        return reverse("agile:agile-detail", args=[value_id])

    def test_unauthenticated_list_view(self, client):
        """Tests get request are allowed for unauthenticated Users."""
        url = reverse("agile:agile-list")
        resp = client.get(url)
        assert resp.status_code == status.HTTP_200_OK

    def test_list_view(self, logged_in_client):
        url = reverse("agile:agile-list")
        resp = logged_in_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

    def test_get_view(self, logged_in_client):
        agile_value = AgileFactory.create(type="value")
        url = self.get_detail_url(agile_value.id)
        resp = logged_in_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

    def test_unauthenticated_get_view(self, client):
        """Tests get request are allowed for unauthenticated Users."""
        agile_value = AgileFactory.create(type="value")
        url = self.get_detail_url(agile_value.id)
        resp = client.get(url)
        assert resp.status_code == status.HTTP_200_OK

    def test_get_filter_value_view(self, logged_in_client):
        AgileFactory.create_batch(4, type="value")
        url = reverse("agile:agile-list")
        resp = logged_in_client.get(url, {"type": Agile.TYPE_VALUE})
        assert resp.status_code == status.HTTP_200_OK
        if len(resp.json()) > 0:
            if "type" in resp.json()[0]:
                assert resp.json()[0]["type"] == Agile.TYPE_VALUE

    def test_get_filter_principle_view(self, logged_in_client):
        AgileFactory.create_batch(12, type="value")
        url = reverse("agile:agile-list")
        resp = logged_in_client.get(url, {"type": Agile.TYPE_PRINCIPLE})
        assert resp.status_code == status.HTTP_200_OK
        if len(resp.json()) > 0:
            if "type" in resp.json()[0]:
                assert resp.json()[0]["type"] == Agile.TYPE_PRINCIPLE

    def test_get_filter_invalid_value_view(self, logged_in_client):
        url = reverse("agile:agile-list")
        resp = logged_in_client.get(url, {"type": "123"})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_unauthenticated_post(self, client, defaults):
        """Tests post request creates a Agile instance."""
        url = reverse("agile:agile-list")
        resp = client.post(url, defaults["payload"])
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_post_type_value(self, logged_in_client, defaults):
        """Tests post request creates a Value instance."""
        url = reverse("agile:agile-list")
        paylod = defaults["payload"]
        paylod.update({"type": Agile.TYPE_VALUE})
        resp = logged_in_client.post(url, defaults["payload"])
        assert resp.status_code == status.HTTP_201_CREATED
        assert validate_uuid4(resp.json()["uuid"])
        agile = Agile.objects.get_or_none(id=resp.json()["id"])
        assert agile is not None
        assert agile.type == Agile.TYPE_VALUE

    def test_post_type_principle(self, logged_in_client, defaults):
        """Tests post request creates a Value instance."""
        url = reverse("agile:agile-list")
        paylod = defaults["payload"]
        paylod.update({"type": Agile.TYPE_PRINCIPLE})
        resp = logged_in_client.post(url, defaults["payload"])
        assert resp.status_code == status.HTTP_201_CREATED
        assert validate_uuid4(resp.json()["uuid"])
        agile = Agile.objects.get_or_none(id=resp.json()["id"])
        assert agile is not None
        assert agile.type == Agile.TYPE_PRINCIPLE

    def test_unauthenticated_patch(self, client, defaults):
        """Tests post request creates a Agile instance."""
        agile_value = AgileFactory.create(type="value")
        url = self.get_detail_url(agile_value.id)
        resp = client.patch(url, defaults["payload"])
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_patch(self, logged_in_client):
        """Tests patch request updates the instance."""
        agile_value = AgileFactory.create(type="value")
        url = self.get_detail_url(agile_value.id)
        payload = {"description": "New Description"}
        resp = logged_in_client.patch(url, payload)
        assert resp.status_code == status.HTTP_200_OK
        agile_value = Agile.objects.get(id=resp.json()["id"])
        assert agile_value.description == payload["description"]

    def test_unauthenticated_put(self, client, defaults):
        """Tests post request creates a Agile instance."""
        agile_value = AgileFactory.create(type="value")
        url = self.get_detail_url(agile_value.id)
        resp = client.put(url, defaults["payload"])
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_put(self, logged_in_client):
        """Tests put request updates an instance."""
        agile_value = AgileFactory.create(type="value")
        url = self.get_detail_url(agile_value.id)
        payload = {"name": "New Name", "description": "New Description"}
        resp = logged_in_client.put(url, payload)
        assert resp.status_code == status.HTTP_200_OK
        agile_value = Agile.objects.get(id=resp.json()["id"])
        assert agile_value.description == payload["description"]
        assert agile_value.name == payload["name"]

    def test_uuid_get(self, logged_in_client):
        agile_value = AgileFactory.create(type="value")
        url = self.get_detail_url(agile_value.id)
        resp = logged_in_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert validate_uuid4(resp.json()["uuid"])
