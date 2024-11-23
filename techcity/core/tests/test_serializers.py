from techcity.core.serializers import BrandSerializer
from techcity.core.tests.factories import BrandFactory


class TestBrandSerializer:
    def test_data(self):
        """The data property returns a dict representing the brand."""
        brand = BrandFactory()
        serializer = BrandSerializer(brand)

        assert serializer.data == {
            "city": brand.city,
            "url": brand.url,
            "name": brand.name,
            "tagline": brand.tagline,
            "description": brand.description,
            "favicon": brand.favicon.name,
            "icon_192x192": brand.icon_192x192.name,
            "icon_512x512": brand.icon_512x512.name,
            "social_image": brand.social_image.name,
        }
