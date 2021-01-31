from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_CPF, validate_phone
from core.models import Base, AddressFields, Clinic, Function
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    is_member = models.BooleanField(default=False)
    is_benefactor = models.BooleanField(default=False)
    is_voluntary = models.BooleanField(default=False)


class ProfileRegistrationData(Base, AddressFields):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField("CPF", unique=True, max_length=14, validators=[validate_CPF])
    birth_date = models.DateField()
    phone_number = models.CharField(validators=[validate_phone], max_length=17, blank=True)


class Member(Base):
    SCHOLARITY_CHOICES = (
        ("ANF", "Analfabeto"),
        ("EFI", "Ensino fundamental incompleto"),
        ("EFC", "Ensino fundamental completo"),
        ("EMI", "Ensino mÃ©dio incompleto"),
        ("EMC", "Ensino mÃ©dio completo"),
        ("ESC", "Superior completo")
    )
    TREATMENT_CHOICES = (
        ("HM", "Hemodiálise"),
        ("DP", "Diálise Peritoneal"),
        ("TP", "Transplantado")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    father_name = models.CharField(max_length=64, blank=True, null=True)
    mother_name = models.CharField(max_length=64, blank=True, null=True)
    companion_name = models.CharField(max_length=64, blank=True, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    is_dead = models.BooleanField(default=False)
    death_date = models.DateField(null=True, blank=True)
    treatment = models.CharField(max_length=3, choices=TREATMENT_CHOICES)
    start_of_treatment = models.DateField(null=True, blank=True)
    scholarity = models.CharField(max_length=4, choices=SCHOLARITY_CHOICES)
    rent = models.FloatField(default=0)
    entry_date = models.DateField(auto_now_add=True)
    departure_date = models.DateField(null=True, blank=True)


class Benefactor(Base):
    user = models.OneToOneField(User, related_name='benefactor', on_delete=models.CASCADE, primary_key=True)


class Voluntary(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)
    departure_date = models.DateField(null=True, blank=True)
