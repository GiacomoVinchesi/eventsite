from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from events.models import Event

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_event_permission(sender, instance, created, **kwargs):
    if instance.user_type == 'organizer':
        try:
            permission = Permission.objects.get(codename='can_create_event')
        except Permission.DoesNotExist:
            content_type = ContentType.objects.get_for_model(Event)
            permission = Permission.objects.create(
                codename='can_create_event',
                name='Può creare eventi',
                content_type=content_type
            )
        instance.user_permissions.add(permission)
