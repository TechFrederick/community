from django.contrib import admin

from .models import Event, Venue


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    pass
