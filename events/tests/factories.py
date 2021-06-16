from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from events.models import Event, EventDonation, Collection, Cost
from donations.tests.factories import DonationFactory


class EventFactory(DjangoModelFactory):

    class Meta:
        model = Event

    event_name = Faker('word')
    start_date = Faker('date_between', start_date='-30d', end_date='-10d')
    end_date = Faker('date_between', start_date='-9d')
    # volunteers
    event_details = Faker('word')
    materials = Faker('word')


class CostFactory(DjangoModelFactory):

    class Meta:
        model = Cost

    cost = Faker('pyfloat', positive=True, min_value=10, max_value=10000)
    details = Faker('word')
    event = SubFactory(EventFactory)


class CollectionFactory(DjangoModelFactory):

    class Meta:
        model = Collection

    collection = Faker('pyfloat', positive=True, min_value=10, max_value=10000)
    details = Faker('word')
    event = SubFactory(EventFactory)


class EventDonationFactory(DonationFactory):

    class Meta:
        model = EventDonation

    event = SubFactory(EventFactory)
