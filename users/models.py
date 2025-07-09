from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    USER_TYPES = [
        ('attendee', 'Attendee'),
        ('organizer', 'Organizer'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPES,
        default='attendee',
        verbose_name="Tipo utente",
        help_text="Seleziona il tipo di utente: partecipante o organizzatore."
    )

    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({'Attendee' if self.user_type == 'attendee' else 'Organizer'})"