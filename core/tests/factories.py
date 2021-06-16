from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from core.models import State, City, Function, AddressFields, Clinic


class StateFactory(DjangoModelFactory):

    class Meta:
        model = State

    name = Faker('word')
    uf = Faker('lexify', text='??', letters='ABCDEF')


class CityFactory(DjangoModelFactory):

    class Meta:
        model = City

    state = SubFactory(StateFactory)
    name = Faker('word')


class FunctionFactory(DjangoModelFactory):

    class Meta:
        model = Function

    name = Faker('word')
    description = Faker('word')


class AddressFieldsFactory(DjangoModelFactory):

    class Meta:
        model = AddressFields
        abstract = True

    state = SubFactory(StateFactory)
    city = SubFactory(CityFactory)
    zip_code = Faker('postcode', locale='pt_BR')
    street = Faker('street_address', locale='pt_BR')
    neighborhood = Faker('word')
    address_number = Faker('word')
    address_complement = Faker('word')


class ClinicFactory(AddressFieldsFactory):

    class Meta:
        model = Clinic

    name = Faker('word')
