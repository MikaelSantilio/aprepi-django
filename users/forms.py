from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from users.models import Benefactor, ProfileRegistrationData, Member
from django.contrib.auth import get_user_model


User = get_user_model()


class MemberForm(forms.ModelForm):

    class Meta(UserCreationForm.Meta):
        model = Member
        fields = '__all__'


class MemberSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_member = True
        user.save()
        Member.objects.create(user=user)

        return user


class BenefactorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_benefactor = True
        user.save()
        Benefactor.objects.create(user=user)

        return user


class ProfileRegistrationDataSignUpForm(forms.ModelForm):
    class Meta:
        model = ProfileRegistrationData
        exclude = ['user', 'active']
