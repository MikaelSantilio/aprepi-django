from django import forms
from donations.models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('donated_value', 'method')
