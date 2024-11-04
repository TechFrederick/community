from django.contrib import admin

from .models import Event, EventRecording, Venue


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "group"]
    list_filter = ["group"]


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    ordering = ["address"]


@admin.register(EventRecording)
class EventRecordingAdmin(admin.ModelAdmin):
    list_display = ["group", "event", "title", "description", "url"]
    list_filter = ["group"]
