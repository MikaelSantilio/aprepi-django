from random import choice

from users.models import ProfileRegistrationData, Member, Voluntary, Benefactor
from django.contrib.auth import get_user_model
from core.tests.factories import FunctionFactory, ClinicFactory
from django.db.models.signals import post_save
from factory import Faker, LazyAttribute, Sequence, SubFactory, django
from factory.django import DjangoModelFactory

User = get_user_model()


@django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    id = Sequence(lambda x: 12345+x)
    username = Sequence(lambda x: f'agent{x}')
    first_name = Faker('first_name', locale='pt_BR')
    last_name = Faker('last_name', locale='pt_BR')

    email = Faker('ascii_free_email', locale='pt_BR')
    password = Faker('password', locale='pt_BR', length=12, digits=True, upper_case=True, lower_case=True)


@django.mute_signals(post_save)
class ProfileRegistrationDataFactory(DjangoModelFactory):

    class Meta:
        model = ProfileRegistrationData

    user = SubFactory(UserFactory)
    cpf = Faker('cpf', locale='pt_BR')
    birth_date = Faker('date_of_birth', minimum_age=18, maximum_age=80)
    phone_number = Faker('lexify', text='(8?)9????-????', letters='1234567890')


class MemberFactory(DjangoModelFactory):

    class Meta:
        model = Member

    user = SubFactory(UserFactory)
    father_name = Faker('word')
    mother_name = Faker('word')
    companion_name = Faker('word')
    clinic = SubFactory(ClinicFactory)
    treatment = LazyAttribute(lambda x: choice(Member.TREATMENT_CHOICES[1:])[0])
    # start_of_treatment
    scholarity = LazyAttribute(lambda x: choice(Member.SCHOLARITY_CHOICES[1:])[0])
    # rent
    # entry_date
    # departure_date


class BenefactorFactory(DjangoModelFactory):

    class Meta:
        model = Benefactor

    user = SubFactory(UserFactory)


class VoluntaryFactory(DjangoModelFactory):

    class Meta:
        model = Voluntary

    user = SubFactory(UserFactory)
    function = SubFactory(FunctionFactory)
    # entry_date
    # departure_date
