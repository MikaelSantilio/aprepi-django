from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    active = models.BooleanField('Active', default=True)

    class Meta:
        abstract = True


class State(models.Model):
    name = models.CharField(max_length=75)
    uf = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.state.uf} - {self.name}"


class Function(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return self.name


class AddressFields(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=9)
    street = models.CharField(max_length=32)
    neighborhood = models.CharField(max_length=32, null=True, blank=True)
    address_number = models.CharField(max_length=8, blank=True, null=True)
    address_complement = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        abstract = True


class Clinic(AddressFields):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
