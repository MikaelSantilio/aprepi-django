from django import forms
from donations.models import Donation, CreditCard
from core.forms import RequestKwargModelFormMixin


class DonationForm(RequestKwargModelFormMixin, forms.ModelForm):

    class Meta:
        model = Donation
        fields = ('donated_value',)


class CreditCardForm(forms.ModelForm):

    class Meta:
        model = CreditCard
        fields = ('number', 'cardholder_name', 'expiration', 'cvv')
