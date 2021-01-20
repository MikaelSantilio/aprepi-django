from django.db import models
from core.models import Base
from users.models import Benefactor


class Donation(Base):

    METHOD_CHOICES = (
        ("CASH", "Em dinheiro"),
        ("PIX", "Pix"),
        ("TED", "Transferência Bancária"),
        ("CREDIT", "Cartão de crédito"),
        ("RCREDIT", "Cartão de crédito - Recorrente"),
    )

    STATUS_CHOICES = (
        ()
    )

    benefactor = models.ForeignKey(Benefactor, null=True, blank=True, on_delete=models.SET_NULL)
    donated_value = models.FloatField()
    method = models.CharField(max_length=6, choices=METHOD_CHOICES)
    status = models.CharField()


class RecurringDonation(Base):
    benefactor = models.ForeignKey(Benefactor, null=True, blank=True, on_delete=models.CASCADE)
    donated_value = models.FloatField()
    has_valid_credit_card = models.BooleanField(default=True)
