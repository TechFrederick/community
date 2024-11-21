from .models import Brand


def brand(request):
    return {"brand": Brand.objects.active()}
