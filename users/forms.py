from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import Benefactor, ProfileRegistrationData, Member, Voluntary
from django.contrib.auth import get_user_model


User = get_user_model()


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['user', 'active', 'is_dead', 'death_date', 'departure_date']


class VoluntaryForm(forms.ModelForm):

    class Meta:
        model = Voluntary
        fields = '__all__'
        exclude = ['user', 'departure_date']


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileRegistrationData
        exclude = ['user', 'active']
