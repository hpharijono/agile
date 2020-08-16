import pytest
import uuid

from typing import Dict

from agile.serializers import AgileSerializer
from agile.tests.factory.agile_factory import AgileFactory


@pytest.mark.django_db
class TestAgileSerializer:
    @pytest.fixture
    def defaults(self) -> Dict[str, Dict[str, str]]:
        agile_fixture = AgileFactory.create()
        uuid_val = uuid.uuid4()
        data = {
            "name": "Responding to change over following a plan.",
            "description": "Circumstances change and sometimes customers demand extra.",
            "uuid": str(uuid_val),
        }
        return {
            "page": agile_fixture,
            "data": data,
        }

    def test_valid(self, defaults):
        serializer = AgileSerializer(data=defaults["data"])
        assert serializer.is_valid(raise_exception=True)

    def test_save(self, defaults):
        serializer = AgileSerializer(data=defaults["data"])
        serializer.is_valid()
        instance = serializer.save()
        assert instance.name == defaults["data"]["name"]
        assert instance.description == defaults["data"]["description"]
        assert str(instance.uuid) == defaults["data"]["uuid"]
