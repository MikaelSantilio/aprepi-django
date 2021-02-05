from django import forms
from users.models import Member
from django.contrib.auth import get_user_model


class MemberupdateForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['user', 'active', 'is_dead', 'death_date', 'departure_date']
