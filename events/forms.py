from django import forms
from events.models import Event, EventDonation
from django.db.models import Q
import datetime


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('event_name', 'start_date', 'end_date', 'volunteers', 'event_details', 'materials')


class EventDonationForm(forms.ModelForm):

    event = forms.ModelChoiceField(
        queryset=Event.objects.filter(Q(end_date__gte=datetime.date.today()) | Q(end_date=None)), required=True)

    class Meta:
        model = EventDonation
        fields = ('donated_value', 'event')
