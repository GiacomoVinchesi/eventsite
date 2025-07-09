from django.urls import path
from .views import (
    HomeView, EventListView, RegisterEventView,
    UnregisterEventView, MyRegistrationsView,
    CreateEventView, MyOrganizedEventsView, DeleteEventView, 
    EventAttendeesView, EditEventView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('events/', EventListView.as_view(), name='view_events'),
    path('events/register/<int:event_id>/', RegisterEventView.as_view(), name='register_event'),
    path('events/unregister/<int:event_id>/', UnregisterEventView.as_view(), name='unregister_event'),
    path('my_registrations/', MyRegistrationsView.as_view(), name='my_registrations'),
    path('create_event/', CreateEventView.as_view(), name='create_event'),
    path('my-organized-events/', MyOrganizedEventsView.as_view(), name='my_organized_events'),
    path('delete-event/<int:event_id>/', DeleteEventView.as_view(), name='delete_event'),
    path('<int:pk>/attendees/', EventAttendeesView.as_view(), name='event_attendees'),
    path('edit_event/<int:pk>/', EditEventView.as_view(), name='edit_event'),
]