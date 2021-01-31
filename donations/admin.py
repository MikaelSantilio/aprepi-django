from django.contrib import admin
from donations.models import CreditCard, Donation, RecurringDonation

admin.site.register(CreditCard)
admin.site.register(Donation)
admin.site.register(RecurringDonation)
