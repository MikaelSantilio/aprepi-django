from django.db import models
from users.models import Base, Voluntary
from donations.models import Donation
from django.core.validators import ValidationError


class Event(Base):
    event_name = models.CharField('Nome do Evento', max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    volunteers = models.ManyToManyField(Voluntary, verbose_name='volunteers', related_name="event_set", blank=True)
    event_details = models.TextField(blank=True, null=True)
    materials = models.TextField(blank=True, null=True)

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError(message='O modelo não condiz com a marca', code='invalid')

    def __str__(self):
        return self.event_name


class Cost(Base):
    cost = models.FloatField('R$0.00')
    details = models.CharField('Detalhes do gasto', max_length=200, blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name='event', related_name="cost_set", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.event_name} - R$ {self.cost:.2f}"


class Collection(Base):
    collection = models.FloatField('R$0.00')
    details = models.CharField('Detalhes do gasto', max_length=200, blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name='event', related_name="collection_set", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.event_name} - R$ {self.collection:.2f}"


class EventDonation(Donation):

    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Donation {self.benefactor.user}"
