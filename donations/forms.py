from django import forms
from donations.models import Donation, CreditCard
from core.forms import RequestKwargModelFormMixin


class DonationForm(RequestKwargModelFormMixin, forms.ModelForm):

    class Meta:
        model = Donation
        fields = ('donated_value', 'method')

        # def clean(self):
        #     cleaned_data = super().clean()
        #     self.cleaned_data["benefactor"] = self.request.user.pk
        #     cleaned_data["benefactor"] = self.request.user.pk
        #     return cleaned_data

        # def save(self):
        #     method = self.cleaned_data.get('method')
        #     donated_value = self.cleaned_data.get('donated_value')
        #     return Donation.objects.create(
        #         donated_value=donated_value, benefactor=benefactor, method=method)


class CreditCardForm(forms.ModelForm):

    class Meta:
        model = CreditCard
        fields = ('number', 'cardholder_name', 'expiration', 'cvv')
