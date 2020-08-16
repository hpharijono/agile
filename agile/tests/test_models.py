import pytest

from agile.models import Agile
from agile.tests.factory.agile_factory import AgileFactory


@pytest.mark.django_db
class TestAgileMethod:
    def test_get_values(self):
        """Tests expected Agile type values from fixtures."""
        AgileFactory.create_batch(4, type="principle")
        AgileFactory.create_batch(3, type="value")
        assert Agile.objects.get_values().count() == 3

    def test_get_principles(self):
        """Tests expected Agile type principles from fixtures."""
        AgileFactory.create_batch(4, type="principle")
        AgileFactory.create_batch(3, type="value")
        assert Agile.objects.get_principles().count() == 4

    def test_get_or_none_found(self):
        """Tests expected Agile instance."""
        AgileFactory.create_batch(7)
        assert isinstance(Agile.objects.get_or_none(id=1), Agile)

    def test_get_or_none(self):
        """Tests expects none."""
        AgileFactory.create_batch(4)
        assert Agile.objects.get_or_none(id=30) is None
