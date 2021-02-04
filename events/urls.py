from django.urls import path
from events import views

app_name = "events"

urlpatterns = [
    path('doacao', views.MakeDonationEventView.as_view(), name='donation'),
    path('', views.EventListView.as_view(), name='list'),
    path('cadastrar', views.EventCreateView.as_view(), name='create'),
    path('atualizar/<int:pk>',
         views.EventUpdateView.as_view(), name='update'),
    path('apagar/<int:pk>',
         views.EventDeleteView.as_view(), name='delete')
]
