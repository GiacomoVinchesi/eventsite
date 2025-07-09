from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        try:
            if user.user_type == 'organizer':
                group = Group.objects.get(name='Organizer')
            else:
                group = Group.objects.get(name='Attendee')
            user.groups.add(group)
        except Group.DoesNotExist:
            pass 

        login(self.request, user)
        return redirect(self.get_success_url())
    


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user
