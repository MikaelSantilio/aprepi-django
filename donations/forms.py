from django import forms
from donations.models import Donation, Benefactor, CreditCard


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('donated_value', 'method')


class DonationByCreditCardForm(forms.Form):

    credit_card = forms.ModelChoiceField(
        queryset=CreditCard.objects.filter(benefactor=request.user.benefactor, valid=True)
    )

    def demand(self):
        # criar a doacao e faz a cobranca no cartao
        pass
    class Meta:
        model = Donation
        fields = ('donated_value', 'method')


class BenefactorForm(forms.ModelForm):
    class Meta:
        model = Benefactor
        fields = ('user')
