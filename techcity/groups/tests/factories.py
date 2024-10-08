import factory


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "groups.Group"

    name = factory.Sequence(lambda n: f"Group {n}")
    slug = factory.Sequence(lambda n: f"group-{n}")
