# from django.contrib.auth.models import AbstractUser
# from django.core.validators import RegexValidator
# from django.db import models
# from users.validators import validate_CPF
# from core.models import State, City


# # class User(AbstractUser):
# #     is_employee = models.BooleanField(default=False)
# #     is_member = models.BooleanField(default=False)
# #     is_benefactor = models.BooleanField(default=False)
# #     is_voluntary = models.BooleanField(default=False)


# class UserCommonFields(models.Model):
#     cpf = models.CharField("CPF", unique=True, max_length=14, validators=[validate_CPF])
#     birth_date = models.DateField()
#     phone_regex = RegexValidator(
#         regex=r'(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})',
#         message="Phone number must be entered in the format: '99 99999-9999'. Up to 15 digits allowed.")
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)


# class Employee(UserCommonFields):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


# class Member(UserCommonFields):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


# class MemberDetail(UserCommonFields):
#     member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True)
#     father_name = models.CharField(max_length=64, blank=True, null=True)
#     mother_name = models.CharField(max_length=64, blank=True, null=True)
#     companion_name = models.CharField(max_length=64, blank=True, null=True)
#     state = models.ForeignKey(State, on_delete=models.CASCADE)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     street = models.ForeignKey()



# class Benefactor(UserCommonFields):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


# class Voluntary(UserCommonFields):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
