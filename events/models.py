from django.db import models
from users.models import Base, Voluntary
from donations.models import Donation


class Event(Base):
    event_name = models.CharField('Nome do Evento', max_length=150, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    volunteers = models.ManyToManyField(
        Voluntary,
        null=True,
        blank=True,
        verbose_name='volunteers',
        related_name="event_set")
    event_details = models.TextField(blank=True, null=True)
    materials = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.event_name


class Cost(Base):
    cost = models.FloatField('R$0.00')
    details = models.CharField('Detalhes do gasto', max_length=200, blank=True, null=True)
    event = models.ManyToManyField(
        Event,
        verbose_name='event',
        related_name="cost_set",)

    def __str__(self):
        return f"{self.event.event_name} - R$ {self.cost:.2f}"


class Collection(Base):
    collection = models.FloatField('R$0.00')
    details = models.CharField('Detalhes do gasto', max_length=200, blank=True, null=True)
    event = models.ManyToManyField(
        Event,
        verbose_name='event',
        related_name="collection_set",)

    def __str__(self):
        return f"{self.event.event_name} - R$ {self.collection:.2f}"


class EventDonation(Donation):

    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Donation {self.benefactor.user}"
