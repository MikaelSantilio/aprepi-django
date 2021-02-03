from django.db import models
from core.models import Base
from donations.validators import FNGCCValidator, card_validator
from users.models import Benefactor
from django.db.models.signals import post_save
from django.dispatch import receiver


class CreditCard(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, validators=[card_validator])
    expiration = models.DateField()
    card_type = models.CharField(max_length=32, blank=True, null=True)
    cardholder_name = models.CharField(max_length=32)
    cvv = models.CharField(max_length=4)
    valid = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Credit Card"
        verbose_name_plural = "Credit Cards"

    def __str__(self):
        return f"Credit Cards {self.benefactor.user}"


class Donation(Base):

    METHOD_CHOICES = (
        ("CASH", "Em dinheiro"),
        ("PIX", "Pix"),
        ("TED", "Transferência Bancária"),
        ("CREDIT", "Cartão de crédito"),
        ("RCREDIT", "Cartão de crédito - Recorrente"),
    )

    STATUS_CHOICES = (
        ("approved", "Aprovado"),
        ("in_process", "Em processo"),
        ("pending", "Pendente"),
        ("authorized", "Autorizado"),
        ("rejected", "Rejeitado"),
        ("charged_back", "Estornado"),
    )

    benefactor = models.ForeignKey(Benefactor, null=True, blank=True, on_delete=models.SET_NULL)
    donated_value = models.FloatField()
    method = models.CharField(max_length=8, choices=METHOD_CHOICES)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Donation {self.benefactor.user}"


class RecurringDonation(Base):
    benefactor = models.ForeignKey(Benefactor, null=True, blank=True, on_delete=models.CASCADE)
    donated_value = models.FloatField()
    has_valid_credit_card = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Recurring Donation"
        verbose_name_plural = "Recurring Donations"

    def __str__(self):
        return f"Donation {self.benefactor.user}"


@receiver(post_save, sender=CreditCard)
def add_card_type(sender, instance, **kwargs):
    post_save.disconnect(add_card_type, sender=sender)

    validator = FNGCCValidator()
    valid_credit_card = validator.creditCard(instance.number)
    if valid_credit_card:
        instance.card_type = valid_credit_card['type']
        instance.save()

    post_save.connect(add_card_type, sender=sender)


post_save.connect(add_card_type, sender=CreditCard)
