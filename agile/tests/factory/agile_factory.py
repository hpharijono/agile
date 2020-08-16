import factory.fuzzy
import factory
from agile.models import Agile


class AgileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Agile

    name = factory.Faker("name")
    type = factory.fuzzy.FuzzyChoice([x[0] for x in Agile.AGILE_TYPES_CHOICES])
