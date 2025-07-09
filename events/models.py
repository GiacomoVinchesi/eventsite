from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)

    description = models.TextField()

    date = models.DateTimeField()

    location = models.CharField(max_length=200)

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events',
        limit_choices_to={'user_type': 'organizer'}
    )
    
    class Meta:
        permissions = [
            ("can_view_all_events", "Può vedere tutti gli eventi"),
            ("can_register_for_event", "Può registrarsi a un evento"),
            ("can_unregister_from_event", "Può annullare la registrazione a un evento"),
            ("can_view_own_registrations", "Può vedere le proprie registrazioni"),
            ("can_create_event", "Può creare eventi"),
            ("can_delete_event", "Può eliminare eventi"),
            ("can_edit_event", "Può modificare eventi"),
            ("can_view_created_events", "Può vedere eventi organizzati"),
            ("can_view_attendees_list", "Può vedere gli iscritti a un evento"),
        ]
        
    def __str__(self):
        return self.title


class Registration(models.Model):
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name='registrations'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'attendee'}
    )

    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    