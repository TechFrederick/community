from django.contrib import admin

from .models import Event, Venue


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_at", "group"]
    list_filter = ["group"]


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    ordering = ["address"]
