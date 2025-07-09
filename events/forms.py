from django import forms
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now():
            raise forms.ValidationError("La data dell'evento non può essere nel passato.")
        return date
