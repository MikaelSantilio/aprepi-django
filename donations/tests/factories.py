from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from donations.models import Donation, RecurringDonation
from users.tests.factories import BenefactorFactory, LazyAttribute
from random import choice


class DonationFactory(DjangoModelFactory):

    class Meta:
        model = Donation

    benefactor = SubFactory(BenefactorFactory)
    donated_value = Faker('pyfloat', positive=True, min_value=10, max_value=10000)
    method = LazyAttribute(lambda x: choice(Donation.METHOD_CHOICES[1:])[0])
    # status


class RecurringDonationFactory(DjangoModelFactory):

    class Meta:
        model = RecurringDonation

    benefactor = SubFactory(BenefactorFactory)
    donated_value = Faker('pyfloat', positive=True, min_value=10, max_value=10000) 

    # has_valid_credit_card
