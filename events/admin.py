from django.contrib import admin
from .models import Event, Registration

# Register your models here.
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registration_date')
    list_filter = ('registration_date',)
    search_fields = ('user__username', 'event__title')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organizer')
    list_filter = ('date', 'organizer')
    search_fields = ('title', 'location')