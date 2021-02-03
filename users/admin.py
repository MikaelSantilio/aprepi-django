from django.contrib import admin
from users.models import ProfileRegistrationData, Member, Benefactor, Voluntary
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(User)
admin.site.register(ProfileRegistrationData)
admin.site.register(Member)
admin.site.register(Benefactor)
admin.site.register(Voluntary)