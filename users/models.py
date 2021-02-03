from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_CPF, validate_phone
from core.models import Base, AddressFields, Clinic, Function


class User(AbstractUser):
    is_member = models.BooleanField(default=False)
    is_benefactor = models.BooleanField(default=False)
    is_voluntary = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)


class ProfileRegistrationData(Base):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField("CPF", unique=True, max_length=14, validators=[validate_CPF])
    birth_date = models.DateField()
    phone_number = models.CharField(validators=[validate_phone], max_length=17, blank=True)

    def __str__(self):
        return f"Profile {self.user}"


class Member(Base):
    SCHOLARITY_CHOICES = (
        (None, "---Escolaridade---"),
        ("ANF", "Analfabeto"),
        ("EFI", "Ensino fundamental incompleto"),
        ("EFC", "Ensino fundamental completo"),
        ("EMI", "Ensino médio incompleto"),
        ("EMC", "Ensino médio completo"),
        ("ESC", "Superior completo")
    )
    TREATMENT_CHOICES = (
        (None, "---Tratamento---"),
        ("HM", "Hemodiálise"),
        ("DP", "Diálise Peritoneal"),
        ("TP", "Transplantado")
    )

    user = models.OneToOneField(User, related_name='member', on_delete=models.CASCADE, primary_key=True)
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

    def __str__(self):
        return f"Member {self.user}"


class Benefactor(Base):
    user = models.OneToOneField(User, related_name='benefactor', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Benefactor {self.user}"


class Voluntary(Base):
    user = models.OneToOneField(User, related_name='voluntary', on_delete=models.CASCADE, primary_key=True)
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)
    departure_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Volunteers"

    def __str__(self):
        return f"Voluntary {self.user}"
