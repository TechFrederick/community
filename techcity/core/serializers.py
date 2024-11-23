from .models import Brand


class BrandSerializer:
    """Serialize a Brand instance.

    This is a custom serializer to avoid pulling in something heavier like DRF.
    """

    def __init__(self, brand: Brand) -> None:
        self.brand = brand

    @property
    def data(self):
        brand = self.brand
        data = {
            "city": brand.city,
            "url": brand.url,
            "name": brand.name,
            "tagline": brand.tagline,
            "description": brand.description,
            "favicon": brand.favicon.name if brand.favicon else "",
            "icon_192x192": brand.icon_192x192.name if brand.icon_192x192 else "",
            "icon_512x512": brand.icon_512x512.name if brand.icon_512x512 else "",
            "social_image": brand.social_image.name if brand.social_image else "",
        }
        return data
