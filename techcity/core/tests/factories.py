import factory


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "core.Brand"

    city = factory.Sequence(lambda n: f"techcity {n}")
    url = factory.Sequence(lambda n: f"https://techcity-{n}.com")
    name = factory.Sequence(lambda n: f"name {n}")
    tagline = factory.Sequence(lambda n: f"tagline {n}")
    description = factory.Sequence(lambda n: f"description {n}")
    favicon = factory.django.FileField()
    icon_192x192 = factory.django.FileField()
    icon_512x512 = factory.django.FileField()
    social_image = factory.django.FileField()
