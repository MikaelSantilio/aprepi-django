from django.contrib import admin
from events import models


admin.site.register(models.Event)
admin.site.register(models.Cost)
admin.site.register(models.Collection)