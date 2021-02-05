from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('doacao/', include('donations.urls', namespace='donations')),
    path('', include('core.urls')),
    path('conta/', include('users.urls', namespace='users')),
    path('evento/', include('events.urls', namespace='events')),
]

urlpatterns += [
    # API base url
    path("api/", include("aprepi.api_router", namespace="api")),
]
