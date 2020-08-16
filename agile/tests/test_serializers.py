import pytest

from typing import Dict

from agile.serializers import AgileSerializer
from agile.tests.factory.agile_factory import AgileFactory


@pytest.mark.django_db
class TestAgileSerializer:
    @pytest.fixture
    def defaults(self) -> Dict[str, Dict[str, str]]:
        agile_fixture = AgileFactory.create()
        data = {
            "name": "Responding to change over following a plan.",
            "description": "Circumstances change and sometimes customers demand extra.",
        }
        return {
            "page": agile_fixture,
            "data": data,
        }

    def test_valid(self, defaults):
        serializer = AgileSerializer(data=defaults["data"])
        assert serializer.is_valid()

    def test_save(self, defaults):
        serializer = AgileSerializer(data=defaults["data"])
        serializer.is_valid()
        instance = serializer.save()
        assert instance.name == defaults["data"]["name"]
        assert instance.description == defaults["data"]["description"]
