from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy
from django.contrib import messages

from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Event, Registration
from .forms import EventForm

# Homepage
class HomeView(TemplateView):
    template_name = 'events/landing_page.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return render(request, 'events/landing_page.html')
        if hasattr(user, 'user_type'):
            if user.user_type == 'attendee':
                return render(request, 'events/landing_page_attendee.html')
            elif user.user_type == 'organizer':
                return render(request, 'events/landing_page_organizer.html')
        return super().get(request, *args, **kwargs)


class EventListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'events.can_view_all_events'
    raise_exception = True  

    model = Event
    template_name = 'events/view_events.html'
    context_object_name = 'events'
    ordering = ['date']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        regs = Registration.objects.filter(user=self.request.user)
        ctx['registered_event_ids'] = {r.event_id for r in regs}
        return ctx


# View per registrarsi a un evento
class RegisterEventView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'events.can_register_for_event'
    raise_exception = True

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if Registration.objects.filter(event=event, user=request.user).exists():
            messages.warning(request, "Sei già registrato a questo evento.")
        else:
            Registration.objects.create(event=event, user=request.user)
            messages.success(request, "Registrazione completata con successo!")
        return redirect('view_events')


# View per annullare la registrazione
class UnregisterEventView(LoginRequiredMixin, View):
    permission_required = 'events.can_unregister_from_event'
    raise_exception = True

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        reg = Registration.objects.filter(event=event, user=request.user).first()
        if reg:
            reg.delete()
            messages.success(request, "Registrazione annullata con successo.")
        else:
            messages.warning(request, "Non sei registrato a questo evento.")

        next_url = request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
            return redirect(next_url)
        return redirect('view_events')


# Lista degli eventi a cui l'utente è registrato
class MyRegistrationsView(LoginRequiredMixin, ListView):
    permission_required = 'events.can_view_own_registrations'
    raise_exception = True

    model = Event
    template_name = 'events/my_registrations.html'
    context_object_name = 'events'

    def get_queryset(self):
        regs = Registration.objects.filter(user=self.request.user).select_related('event')
        return [r.event for r in regs]


# Creazione evento (solo organizer con permesso)
class CreateEventView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'events.can_create_event'
    raise_exception = True

    model = Event
    form_class = EventForm
    template_name = 'events/create_event.html'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Evento creato con successo!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


# Lista degli eventi organizzati dall'utente (solo organizer con permesso)
class MyOrganizedEventsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'events.can_view_created_events'
    raise_exception = True

    model = Event
    template_name = 'events/my_organized_events.html'
    context_object_name = 'events'
    permission_required = 'events.can_create_event'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)


# Eliminazione evento (solo organizer con permesso)
class DeleteEventView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'events.can_delete_event'
    raise_exception = True

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, organizer=request.user)
        event.delete()
        return redirect('my_organized_events')
    

class EventAttendeesView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'events.can_view_attendees_list'
    raise_exception = True

    model = Event
    template_name = 'events/event_attendees.html'
    context_object_name = 'event'

    def get_queryset(self):
        # Limita la visualizzazione agli eventi creati dall'utente
        return Event.objects.filter(organizer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attendees'] = Registration.objects.filter(
            event=self.object
        ).select_related('user')
        return context
    
class EditEventView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/edit_event.html'
    permission_required = 'events.can_edit_event'

    def get_queryset(self):
        # Limita la modifica solo agli eventi organizzati dall'utente
        return Event.objects.filter(organizer=self.request.user)

    def get_success_url(self):
        return reverse_lazy('my_organized_events')
