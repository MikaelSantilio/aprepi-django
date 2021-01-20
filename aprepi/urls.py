from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fazer-doacao/', include('donations.urls')),
    path('minha-conta/', include('users.urls')),
]
