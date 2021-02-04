from django.db import models
from users.models import Base, Voluntary


class Event(Base):
    event_name = models.CharField('Nome do Evento', max_length=150, blank=True, null=True)
    date_event = models.DateTimeField()

    volunteers = models.ManyToManyField(
        Voluntary,
        verbose_name='volunteers',
        related_name="evento_set",)
    event_details = models.TextField()
    materials = models.TextField()


class Cost(Base):
    cost = models.FloatField('R$0.00')
    details = models.CharField('Detalhes do gasto', max_length=200, blank=True, null=True)
    event = models.ManyToManyField(
        Event,
        verbose_name='event',
        related_name="cost_set",)


class Collection(Base):
    collection = models.FloatField('R$0.00')
    details = models.CharField('Detalhes do gasto', max_length=200, blank=True, null=True)
    event = models.ManyToManyField(
        Event,
        verbose_name='event',
        related_name="collection_set",)
