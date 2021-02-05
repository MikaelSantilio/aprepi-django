from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
   openapi.Info(
      title="UP Revendas API",
      default_version='v1',
      description="Exemplo de API para sistema de loja de veículos",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mikael.santilio@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

app_name = "api"

urlpatterns = [
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("docs/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("evento/", include('events.api.urls', namespace='events')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
