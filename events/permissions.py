from django.core.exceptions import PermissionDenied

def is_organizer(user):
    return user.user_type == 'Organizer'

def is_attendee(user):
    return user.user_type == 'Attendee'

class OrganizerRequiredMixin:
    """Mixin per viste che richiedono un utente Organizer"""
    def dispatch(self, request, *args, **kwargs):
        if not is_organizer(request.user):
            raise PermissionDenied("Solo gli organizzatori possono accedere a questa pagina.")
        return super().dispatch(request, *args, **kwargs)

class AttendeeRequiredMixin:
    """Mixin per viste che richiedono un utente Attendee"""
    def dispatch(self, request, *args, **kwargs):
        if not is_attendee(request.user):
            raise PermissionDenied("Solo i partecipanti possono accedere a questa pagina.")
        return super().dispatch(request, *args, **kwargs)