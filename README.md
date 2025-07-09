# Event Organizer Web App

## Description

This project is a web platform for event management that allows two types of users to interact:

- **Organizer**: users who can create, edit, delete events, and view who registered.
- **Attendee**: users who can view available events, register for them, and cancel their registrations.

The platform includes authentication, permission management via groups, and specific functions for each user type.

---

## Main Features

### For Organizers

- Register and log in as an organizer.
- Create new events with title, description, date, and location.
- Edit and delete their created events.
- View a list of their organized events.
- View the list of attendees registered for each event.

### For Attendees

- Register and log in as an attendee.
- View a list of all available events.
- Register for events.
- Cancel their event registrations.
- View their own registrations.

---

## How to Use the Site

### Registration and Login

1. **Register** by choosing your user type (Organizer or Attendee).
2. **Log in** with the created credentials.

### For Organizers

- After logging in, access the **Organizer dashboard**.
- From there you can:
  - View all available events and register for them.
  - View and manage your registrations.
  - Create a new event via the “Create Event” button.
  - Manage your events (edit, delete).
  - View the attendees registered for your events.

### For Attendees

- After logging in, access the **Attendee dashboard**.
- From there you can:
  - View all available events.
  - Register for events.
  - View and manage your registrations.

---

## Restrictions and Permissions

- Only **Organizers** can create, edit, or delete events and see the list of attendees for the events created by the,. 
- Actions are controlled by Django permissions assigned to groups (`Organizer` and `Attendee`).
