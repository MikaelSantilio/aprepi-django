from django.db import models


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