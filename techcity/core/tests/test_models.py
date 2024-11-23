from techcity.core.models import Brand
from techcity.core.tests.factories import BrandFactory


class TestBrand:
    def test_active(self):
        """An active brand is returned if it exists."""
        brand = BrandFactory()

        active_brand = Brand.objects.active()

        assert active_brand == brand

    def test_urls(self):
        """URL properties return the media file URL."""
        brand = BrandFactory()

        assert brand.favicon_url == brand.favicon.url
        assert brand.icon_192x192_url == brand.icon_192x192.url
        assert brand.icon_512x512_url == brand.icon_512x512.url
        assert brand.social_image_url == brand.social_image.url
