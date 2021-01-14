from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_CPF


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_benefactor = models.BooleanField(default=False)
    is_voluntary = models.BooleanField(default=False)


class UserCommonFields(models.Model):
    cpf = models.CharField("CPF", unique=True, max_length=14, validators=[validate_CPF])
    birth_date = models.DateField()


class Employee(UserCommonFields):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Member(UserCommonFields):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Benefactor(UserCommonFields):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Voluntary(UserCommonFields):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
