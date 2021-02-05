from django.urls import path
from rest_framework.routers import DefaultRouter

from events.api import views

app_name = "events"

router = DefaultRouter()


router.register('', views.EventViewSet, basename="events")

urlpatterns = [
    # path("doacao/", views.EventDonationCreateAPIView.as_view(), name="donation"),
    path("despesa/", views.CostListCreateAPIView.as_view(), name="cost-list"),
    path("despesa/<int:pk>/", views.CostRetrieveUpdateDestroyAPIView.as_view(), name="cost-detail"),
    path("arrecadacao/", views.CollectionListCreateAPIView.as_view(), name="collection-list"),
    path("arrecadacao/<int:pk>/", views.CollectionRetrieveUpdateDestroyAPIView.as_view(), name="collection-detail"),
]

urlpatterns += router.urls
