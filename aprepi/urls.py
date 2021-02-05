from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('doacao/', include('donations.urls', namespace='donations')),
    path('', include('core.urls')),
    path('conta/', include('users.urls', namespace='users')),
    path('socio/', include('member.urls', namespace='member')),
]
